---
name: ael-ledger-setup
description: Use this skill to design and add an Agent Execution Ledger (AEL) to any agent/pipeline project — an append-only SQLite structure that records every decision cycle as Planning -> Execution -> Evidence -> Verification -> Reflection -> State (a single source of truth), so decisions stay auditable and explainable after the fact. Trigger whenever the user asks to add a "ledger", "AEL", "실행 기록 시스템", "decision trace", "audit trail", "explainability layer", or wants an agent's decisions to be debuggable/traceable/provable-not-a-black-box — even if they never say "AEL" explicitly (e.g. "이 에이전트가 왜 이렇게 판단했는지 나중에 확인할 수 있게 해줘", "add an audit log for the router's decisions", "심사위원한테 판단 근거를 보여줘야 해").
---

# Skill: Agent Execution Ledger (AEL) 구축하기

## 개요
AEL은 에이전트 파이프라인의 각 결정 사이클을 6단계로 기록하는 append-only SSOT(Single Source of Truth)다.

- **목적 1 — 설명 가능성**: 특정 결정이 왜 그렇게 났는지 사후에 정확히 역추적.
- **목적 2 — 환각 방지**: "에이전트가 했다고 주장하는 것"과 "실제로 검증을 통과한 것"을 구조적으로 분리 (Verification 없이는 State가 갱신되지 않는다).
- 특정 프로젝트 전용 설계가 아니라, 어떤 에이전트/파이프라인에도 적용 가능한 범용 절차다.

## 핵심 원칙
**AEL은 새 로직을 만드는 게 아니라, 기존 파이프라인이 이미 하는 일을 구조화해서 기록하는 것**이다. 프롬프트나 판단 로직을 새로 설계하지 않는다 — 기존 함수가 이미 만들어내는 reason/confidence/evidence 같은 필드를 그대로 재사용한다. 6단계 중 일부가 그 프로젝트에 자연스럽게 없다면 억지로 채우지 말고 비워두거나 인접 단계에 병합해도 된다.

## 1단계: 대상 프로젝트의 파이프라인 파악
코드를 읽고 다음을 파악한다:
- 무엇이 "하나의 사이클"인가? (메시지 1건, API 요청 1건, 태스크 1건 등 — 이게 `cycle_id`가 된다)
- 그 사이클 안에서 이미 자연스럽게 생성되는 데이터는? (판단 근거, 확신도, 인용 자료 등 — 있으면 재사용)
- 기존 저장소가 있는가? (SQLite/파일 캐시 등) — 있다면 그 컨벤션(연결 헬퍼, 테이블 명명 규칙)을 따른다
- 기존 DB가 매 실행마다 재빌드/드롭되는가? AEL은 절대 그 재빌드 대상에 포함되면 안 된다 — 별도 파일(예: `data/ael.db`)로 분리한다. AEL은 입력 데이터의 사본이 아니라 "에이전트가 실제로 한 일"의 기록이기 때문이다.

## 2단계: 6단계를 프로젝트에 매핑
| 단계 | 질문 | 코드에서 찾을 곳 |
|---|---|---|
| Planning | 이번 사이클에서 무엇을 하려 하는가? | 사이클 시작 시 입력/컨텍스트를 모으는 코드 |
| Execution | 실제로 무엇을 했는가? | 모델 호출, 툴 호출, 핵심 로직 실행 지점 |
| Evidence | 그 결정을 뒷받침하는 근거는? | 인용된 데이터, 검색 결과, 첨부 자료 |
| Verification | 근거가 결과를 정당화하는가? | 스키마 검증, 허용값 체크, confidence 계산 |
| Reflection | 왜 이렇게 됐고, 다음은? | 실패 원인, 내부 판단 필드, 재시도 플래그 |
| State | 지금 무엇을 알고 있는가? | 최종 출력/결과물 (압축 체크포인트) |

## 3단계: 범용 SQLite 스키마 템플릿
```sql
CREATE TABLE IF NOT EXISTS ael_planning (
    plan_id    TEXT PRIMARY KEY,      -- "{cycle_id}:plan"
    cycle_id   TEXT NOT NULL,
    goal       TEXT NOT NULL,
    inputs     TEXT,                  -- JSON
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS ael_execution (
    exec_id    TEXT PRIMARY KEY,      -- "{cycle_id}:exec"
    plan_id    TEXT REFERENCES ael_planning(plan_id),
    cycle_id   TEXT NOT NULL,
    action     TEXT,
    tool_calls TEXT,                  -- JSON
    status     TEXT CHECK(status IN ('success','failed')),
    ended_at   TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS ael_evidence (
    evidence_id   TEXT PRIMARY KEY,
    exec_id       TEXT REFERENCES ael_execution(exec_id),
    cycle_id      TEXT NOT NULL,
    evidence_type TEXT,
    ref_id        TEXT,
    detail        TEXT,
    collected_at  TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS ael_verification (
    verify_id   TEXT PRIMARY KEY,     -- "{cycle_id}:verify"
    exec_id     TEXT REFERENCES ael_execution(exec_id),
    cycle_id    TEXT NOT NULL,
    criteria    TEXT,
    result      TEXT CHECK(result IN ('pass','fail','partial')),
    confidence  REAL,
    verified_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS ael_reflection (
    reflect_id  TEXT PRIMARY KEY,     -- "{cycle_id}:reflect"
    verify_id   TEXT REFERENCES ael_verification(verify_id),
    cycle_id    TEXT NOT NULL,
    what_failed TEXT,
    root_cause  TEXT,
    next_action TEXT,
    created_at  TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS ael_state (
    state_id        TEXT PRIMARY KEY,  -- "{cycle_id}:state:{timestamp}"
    cycle_id        TEXT NOT NULL,
    reflect_id      TEXT REFERENCES ael_reflection(reflect_id),
    snapshot        TEXT NOT NULL,     -- JSON: 최종 결과
    checkpoint_type TEXT CHECK(checkpoint_type IN ('cycle_end','retry','manual')),
    created_at      TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_ael_planning_cycle     ON ael_planning(cycle_id);
CREATE INDEX IF NOT EXISTS idx_ael_execution_cycle    ON ael_execution(cycle_id);
CREATE INDEX IF NOT EXISTS idx_ael_evidence_cycle     ON ael_evidence(cycle_id);
CREATE INDEX IF NOT EXISTS idx_ael_verification_cycle ON ael_verification(cycle_id);
CREATE INDEX IF NOT EXISTS idx_ael_reflection_cycle   ON ael_reflection(cycle_id);
CREATE INDEX IF NOT EXISTS idx_ael_state_cycle        ON ael_state(cycle_id);
```
프로젝트의 실제 사이클 식별자(message_id, request_id, task_id 등)로 `cycle_id`를 대체한다. 테이블/컬럼명을 도메인 용어로 바꿔도 되지만, 6단계 구조와 FK 체인(각 단계가 이전 단계를 참조)은 유지한다.

## 4단계: 클라이언트 코드 템플릿
```python
import json
import sqlite3
from pathlib import Path

DB_PATH = Path("data/ael.db")          # 기존 작업 DB와 반드시 분리
SCHEMA_PATH = Path(__file__).parent / "ael_schema.sql"


def get_connection(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path=DB_PATH):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        conn.commit()
    finally:
        conn.close()


def record_cycle(cycle_id, planning, execution, evidence, verification,
                  reflection, state, conn=None):
    """한 번의 호출로 6단계를 모두 기록한다. 각 인자는 해당 테이블의
    컬럼명을 키로 갖는 dict (evidence만 dict의 리스트). INSERT OR REPLACE로
    "{cycle_id}:단계" 형태의 PK를 써서, 재시도가 같은 사이클을 덮어쓰되
    다른 사이클과는 절대 섞이지 않게 한다."""
    owns = conn is None
    conn = conn or get_connection()
    try:
        # ... 각 테이블에 INSERT OR REPLACE — 실제 예시는 아래 참고 구현의
        # ael_client.py의 record_cycle()을 그대로 본떠 프로젝트 필드명에 맞게 고친다.
        if owns:
            conn.commit()
    finally:
        if owns:
            conn.close()


def get_cycle(cycle_id, conn=None):
    """Planning부터 State까지 전체 이력을 재구성 — ael-ssot-debug 스킬에서 사용."""
    ...
```

**참고 구현(전체 코드)**: `C:\Users\abab9\Desktop\hackerrank-orchestrate-august26\hackerrank-orchestrate-august26\code\ael_schema.sql`, `...\code\ael_client.py`. WhatsApp 메시지 라우터 전용으로 필드명이 붙어 있지만 (message_id, sender_trust 등), `record_cycle`/`get_cycle` 패턴과 6단계 테이블 구조는 그대로 재사용 가능한 완성된 예시다. 이 파일을 복사해 프로젝트의 도메인 필드명으로 바꾸는 것이 빈 템플릿에서 시작하는 것보다 빠르다.

## 5단계: 기존 파이프라인에 최소 침습적으로 연결
- 기존 함수의 반환값을 그대로 `record_cycle()`에 넘긴다 — 프롬프트나 판단 로직은 건드리지 않는다.
- 사이클 처리 함수 안, 결과가 나온 직후 한 줄(`record_cycle(...)`)만 추가하는 것을 목표로 한다.
- 기존 DB 재빌드/드롭 로직과 AEL DB가 절대 겹치지 않는지 다시 한번 확인한다.

## 6단계: 검증
```bash
python -c "
import sqlite3
conn = sqlite3.connect('_ael_test.db')
conn.executescript(open('ael_schema.sql', encoding='utf-8').read())
tables = [r[0] for r in conn.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall()]
print(sorted(tables))
"
```
6개 테이블이 모두 출력되면 스키마가 유효하다. 그 다음 실제 사이클 1건을 처리시켜 `get_cycle()`로 6단계가 다 채워졌는지 확인한다.

## 검증 포인트
- [ ] 6개 테이블이 오류 없이 생성됨
- [ ] 기존 파이프라인의 로직/프롬프트는 수정하지 않음 (감사 계층만 추가)
- [ ] AEL DB가 기존 캐시/작업 DB의 재빌드·드롭 로직과 분리되어 있음
- [ ] 실제 사이클 1건 처리 후 `get_cycle()`로 6단계가 모두 조회됨

## 관련 스킬
- 구축한 AEL을 실제로 디버깅에 활용하려면 `ael-ssot-debug` 스킬을 사용한다.
