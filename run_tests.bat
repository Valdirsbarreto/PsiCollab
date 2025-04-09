@echo off
echo Executando testes do PsiCollab...

REM Instala ou atualiza dependências
pip install -r requirements.txt

REM Executa todos os testes com cobertura
pytest --cov=. tests/

echo.
echo Testes concluídos!
pause 