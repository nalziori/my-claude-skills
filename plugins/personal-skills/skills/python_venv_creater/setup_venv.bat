@echo off
REM ============================================
REM  Python 가상환경 생성 및 설정 자동화 스크립트
REM  사용법: setup_venv.bat [python버전]
REM  예시:   setup_venv.bat 3.11
REM ============================================

setlocal

REM 사용할 Python 버전 (기본값: 3.11)
if "%1"=="" (
    set PYVER=3.11
) else (
    set PYVER=%1
)

echo [1/6] Python %PYVER% 가상환경 생성 중...
py -%PYVER% -m venv .venv
if errorlevel 1 (
    echo [오류] 가상환경 생성 실패. Python %PYVER% 설치 여부를 확인하세요.
    exit /b 1
)

echo [2/6] pip 업그레이드 중...
.venv\Scripts\python -m pip install --upgrade pip

echo [3/6] 핵심 패키지 설치 중 (numpy, pandas, ipykernel, jupyter)...
.venv\Scripts\pip install numpy pandas ipykernel jupyter

echo [4/6] requirements.txt 존재 시 의존성 설치 중...
if exist requirements.txt (
    .venv\Scripts\pip install -r requirements.txt
)

echo [5/6] Jupyter 커널 등록 중...
.venv\Scripts\python -m ipykernel install --user --name project2-venv --display-name "Python (.venv) project2"

echo [6/6] 설치 확인...
.venv\Scripts\pip list

echo.
echo ============================================
echo  가상환경 구성 완료!
echo  활성화: .venv\Scripts\activate
echo  실행:   python hello.py
echo ============================================

endlocal
