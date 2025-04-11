import os

print("Iniciando setup do ambiente DevContainer...")

# Cria .devcontainer
os.makedirs(".devcontainer", exist_ok=True)

# devcontainer.json
with open(".devcontainer/devcontainer.json", "w", encoding="utf-8") as f:
    f.write("""{
  "name": "PsiCollab DevContainer",
  "dockerComposeFile": "../docker-compose.yml",
  "service": "web",
  "workspaceFolder": "/app",
  "extensions": [
    "ms-python.python",
    "ms-azuretools.vscode-docker",
    "ms-vscode.makefile-tools"
  ],
  "settings": {
    "python.pythonPath": "/usr/local/bin/python",
    "terminal.integrated.defaultProfile.linux": "bash"
  },
  "postCreateCommand": "pip install -r requirements.txt",
  "remoteEnv": {
    "PYTHONPATH": "/app"
  }
}""")

# Dockerfile
with open(".devcontainer/Dockerfile", "w", encoding="utf-8") as f:
    f.write("""FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
""")

# pytest.ini
with open("pytest.ini", "w", encoding="utf-8") as f:
    f.write("""[pytest]
addopts = -ra -q
testpaths = tests
pythonpath = .
""")

# Garante __init__.py em app/
os.makedirs("app", exist_ok=True)
with open("app/__init__.py", "w", encoding="utf-8") as f:
    pass

# Script Windows para rodar pytest
with open("run_tests.bat", "w", encoding="utf-8") as f:
    f.write("""@echo off
set PYTHONPATH=%cd%
pytest -v
pause
""")

print("Setup concluído!")
print("Agora é só abrir o VSCode e usar: Dev Containers -> Reopen in Container")
print("Para rodar os testes no Windows, execute: run_tests.bat") 