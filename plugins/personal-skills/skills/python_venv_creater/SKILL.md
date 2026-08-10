---
name: python_venv_creater
description: Use this skill to create and configure a Python virtual environment (.venv) for a project — creating the venv, upgrading pip, installing dependencies (from requirements.txt or core packages), registering a Jupyter kernel, and wiring up VSCode settings. Trigger on requests like "set up a venv", "create a virtual environment", "python 가상환경 만들어줘".
---

# Skill: Python 가상환경 구성하기

디렉터리에 Python 가상환경(virtual environment)을 생성하고, 개발에 필요한 패키지를 설치하며, VSCode/Jupyter에서 사용할 수 있도록 환경을 구성하는 과정을 다룹니다.

## 개요
- Python 프로젝트를 진행할 때 시스템 전역 파이썬 환경과 분리된 격리된 실행 환경을 만듭니다.
- 프로젝트별로 의존성(package)을 독립적으로 관리할 수 있습니다.
- VSCode와 Jupyter Notebook에서 가상환경을 자동으로 감지/사용하도록 설정합니다.

## 사전 준비
- Python 설치 확인: `python --version`
- 여러 Python 버전이 설치된 경우 `py -3.x` 와 같은 launcher 사용 가능
- `requirements.txt` 파일 존재 여부 확인 (프로젝트 의존성 목록)

## 스킬 단계

### 1단계: 환경 및 프로젝트 구조 파악
1. 현재 디렉터리의 파일 목록을 확인한다.
   - `list_files` 또는 `search_files`로 프로젝트 구조 파악
2. `requirements.txt`가 있으면 읽어서 설치할 의존성을 파악한다.
3. `hello.py`, `test.py` 등 실행/테스트 파일을 확인한다.

### 2단계: 사용할 Python 버전 결정
- 시스템 기본 파이썬 버전 확인: `python --version`
- `where python` (Windows) 또는 `which python` (macOS/Linux)로 설치된 파이썬 경로 확인
- 프로젝트 의존성 호환성에 맞는 버전 선택 (예: pandas/numpy가 특정 버전을 요구할 경우)

### 3단계: 가상환경 생성
```bash
# Windows (Python 3.11 사용 예시)
py -3.11 -m venv .venv

# 또는 특정 python 실행파일 지정
python -m venv .venv
```
- 생성 확인: `.venv/` 폴더에 `Scripts/`(Windows) 또는 `bin/`(macOS/Linux) 생성 확인

### 4단계: pip 업그레이드
```bash
.venv\Scripts\python -m pip install --upgrade pip
```

### 5단계: 패키지 설치
```bash
# requirements.txt 존재 시
.venv\Scripts\pip install -r requirements.txt

# 핵심 패키지 직접 설치
.venv\Scripts\pip install numpy pandas ipykernel jupyter
```

### 6단계: 설치 검증
```bash
.venv\Scripts\python -c "import pandas, numpy; print(pandas.__version__, numpy.__version__)"
.venv\Scripts\python hello.py
```

### 7단계: VSCode 연동 설정
`.vscode/settings.json` 생성:
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
  "python.terminal.activateEnvironment": true,
  "python.terminal.activateEnvInCurrentTerminal": true,
  "jupyter.interactiveWindowMode": "perCell",
  "jupyter.jupyterServerType": "local"
}
```

### 8단계: Jupyter 커널 등록 (Notebook 사용 시)
```bash
.venv\Scripts\python -m ipykernel install --user --name <커널이름> --display-name "<표시이름>"
```

### 9단계: 의존성 목록 저장 및 문서화
```bash
.venv\Scripts\pip freeze > requirements.txt
```
- README.md에 가상환경 사용법(활성화/비활성화/패키지 설치/실행) 문서화

## 주의사항
- pip 설치 시 출력이 중간에 잘려 보여도 실제로 설치가 완료될 수 있으므로, `pip list`로 재확인한다.
- `requirements.txt`에 존재하지 않는 버전이 있을 수 있으므로, 설치 실패 시 유효한 버전으로 대체 설치한다.
- 가상환경은 `.venv/` 디렉터리를 소스코드 관리를 위해 `.gitignore`에 추가하는 것이 좋다.

## 검증 포인트
- [ ] `.venv/` 폴더 생성 확인
- [ ] `pip list`로 필요한 패키지 설치 확인
- [ ] `python <스크립트>.py` 실행 정상 동작 확인
- [ ] VSCode에서 가상환경 자동 선택 확인
- [ ] Jupyter Notebook에서 커널 선택 가능 확인

## 완료 예시
이 스킬을 적용한 결과물:
- `.venv/` 가상환경 생성
- `requirements.txt` 갱신
- `.vscode/settings.json` 추가
- `README.md`에 사용법 문서화
- Jupyter 커널 "Python (.venv) <프로젝트명>" 등록
