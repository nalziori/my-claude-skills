---
name: ael-ssot-debug
description: Use this skill when a project already has an Agent Execution Ledger (AEL) — tables like ael_planning/ael_execution/ael_evidence/ael_verification/ael_reflection/ael_state, or a similarly named decision ledger — and the user wants to understand or debug why a specific decision/cycle happened the way it did. Trigger on requests like "이 message_id 왜 mute로 판단됐는지 확인해줘", "이 케이스 왜 실패했는지 AEL로 추적해줘", "confidence 낮은 애들 패턴 좀 찾아줘", "왜 이렇게 판단했는지 로그/원장에서 찾아봐줘", or any debugging question about an agent's past decision in a project with a ledger — even before assuming the fix requires reading or changing code.
---

# Skill: AEL을 SSOT로 활용한 디버깅

## 핵심 원칙
**코드를 다시 읽고 추측하기 전에, 원장(ledger)을 먼저 읽어라.** AEL이 있는 프로젝트에서 특정 결정이 왜 그렇게 났는지 궁금하면, 프롬프트나 로직을 눈으로 재추론하지 말고 그 사이클의 실제 기록을 조회해서 무슨 일이 있었는지 먼저 확인한다. 코드는 "무엇을 하려 했는가"를 보여주지만, AEL은 "실제로 무슨 일이 일어났는가"를 보여준다 — 이 둘은 다를 수 있고, 다를 때 진짜 버그가 있다.

## 언제 쓰는가
- 특정 케이스(message_id, request_id 등)가 왜 특정 결과로 분류/처리됐는지 설명해야 할 때
- confidence가 낮거나 실패로 표시된 케이스들의 공통 패턴을 찾아야 할 때
- "이 에이전트는 블랙박스가 아니다"를 실제로 증명해야 할 때 (심사, 감사, 사용자 문의 대응)

## 절차: 역방향 추적 (State → Planning)
State부터 시작해 이전 단계로 거슬러 올라간다 — "지금 뭘 알고 있나"에서 "애초에 뭘 하려 했나" 방향으로. 프로젝트에 `get_cycle(cycle_id)` 같은 헬퍼가 이미 있으면 그걸 먼저 쓰고, 없으면 아래 SQL을 순서대로 직접 실행한다.

### 1. State — 최종 결과가 뭐였나
```sql
SELECT * FROM ael_state WHERE cycle_id = ? ORDER BY created_at DESC LIMIT 1;
```
최종 결과와, 그게 어떤 `reflect_id`에서 나왔는지 확인한다.

### 2. Reflection — 내부 판단 신호가 뭐였나
```sql
SELECT * FROM ael_reflection WHERE reflect_id = ?;
```
내부 판단 필드(신뢰도/위험도/긴급도 등 프로젝트별로 다름)와 `next_action`(재시도 필요 여부)을 확인한다. "왜 이 방향으로 판단했는가"의 1차 답이 여기 있다.

### 3. Verification — 검증을 통과했나, confidence는 얼마였나
```sql
SELECT * FROM ael_verification WHERE verify_id = ?;
```
스키마/값 검증이 실패했다면 여기서 바로 드러난다 — Reflection의 판단이 애초에 검증되지 않은 주장이었을 수 있다.

### 4. Evidence — 어떤 근거를 인용했고, 그게 타당한가
```sql
SELECT * FROM ael_evidence WHERE exec_id = ?;
```
인용된 근거의 `detail`을 직접 읽어본다. 근거가 빈약하거나 무관하면 Verification의 실패와 함께 원인이 드러난다.

### 5. Execution — 실제로 어떤 모델/툴 호출이 있었나
```sql
SELECT * FROM ael_execution WHERE exec_id = ?;
```
status, 사용된 모델/도구, 캐시 히트 여부 확인 — 예상과 다른 설정으로 실행됐을 수 있다.

### 6. Planning — 애초에 무엇을 계획했나
```sql
SELECT * FROM ael_planning WHERE plan_id = ?;
```
어떤 컨텍스트를 모으기로 계획했는지 확인한다. 필요한 컨텍스트가 계획 단계에서부터 빠져 있었다면, 그 이후 모든 단계는 처음부터 잘못된 입력 위에서 진행된 것이다 — 실행/프롬프트를 고치기 전에 이 가능성부터 배제한다.

## 여러 실패 케이스 비교로 패턴 찾기
개별 케이스가 아니라 "왜 특정 유형이 자주 틀리는가"를 알고 싶을 때:
```sql
-- 재시도가 필요하다고 표시된 케이스들
SELECT cycle_id, root_cause FROM ael_reflection WHERE next_action = 'flag_for_retry';

-- confidence가 낮은 케이스들
SELECT cycle_id, confidence FROM ael_verification WHERE confidence < 0.5 ORDER BY confidence ASC;

-- 검증 실패 케이스들의 공통 root_cause
SELECT r.root_cause, COUNT(*) FROM ael_reflection r
JOIN ael_verification v ON v.verify_id = r.verify_id
WHERE v.result != 'pass' GROUP BY r.root_cause ORDER BY COUNT(*) DESC;
```
같은 `root_cause`나 같은 내부 신호 값이 반복된다면, 개별 케이스를 하나씩 고치는 게 아니라 프롬프트/로직 자체를 고쳐야 한다는 신호다.

## 원장에 원인이 없을 때
6단계를 다 조회했는데도 원인이 안 보인다면, 그건 AEL 자체의 계측이 부족하다는 신호다 — 코드를 억지로 재추론하기 전에 어떤 필드가 빠져서 이 케이스를 설명하지 못했는지 확인하고, `ael-ledger-setup` 스킬로 계측을 보강하는 것을 먼저 고려한다.

## 검증 포인트
- [ ] 코드를 재추론하기 전에 실제 AEL 레코드를 먼저 조회했다
- [ ] State에서 시작해 Planning까지 FK 체인을 따라갔다
- [ ] 실패 케이스가 여럿이면 개별이 아니라 공통 패턴을 찾았다
- [ ] 원인을 코드 수정 없이 "기록에서" 먼저 설명할 수 있었다

## 관련 스킬
- AEL을 아직 구축하지 않은 프로젝트라면 `ael-ledger-setup` 스킬을 먼저 사용한다.
