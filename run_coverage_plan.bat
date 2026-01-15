@echo off
echo ==========================================
echo  ISAB TimeSheet - Test Coverage Plan
echo ==========================================

if not exist .venv (
    echo [ERROR] Virtual environment not found!
    exit /b 1
)

echo [1/3] Updating dependencies...
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pip install pytest pytest-cov pytest-qt pytest-mock pytest-asyncio

echo [2/3] Running Tests with Coverage...
.venv\Scripts\python.exe -m pytest --cov=src --cov-report=html --cov-report=term-missing tests/

echo [3/3] Done. Report generated at htmlcov/index.html
pause
