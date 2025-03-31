"""
Testes para o sistema de auditoria.
"""
import pytest
import json
import os
from datetime import datetime, timedelta
from app.core.audit import (
    AuditoriaManager,
    TipoOperacao,
    NivelSensibilidade,
    RegistroAuditoria
)

@pytest.fixture
def audit_manager():
    """Fixture que cria uma instância do gerenciador de auditoria."""
    return AuditoriaManager()

@pytest.fixture
def registro_exemplo():
    """Fixture que cria um registro de auditoria de exemplo."""
    return {
        "tipo_operacao": TipoOperacao.LEITURA,
        "nivel_sensibilidade": NivelSensibilidade.ALTO,
        "usuario_id": "user123",
        "recurso": "teste_psicologico",
        "detalhes": {
            "teste_id": "test123",
            "tipo_teste": "WAIS-IV"
        },
        "ip_address": "192.168.1.1",
        "user_agent": "Mozilla/5.0",
        "metadata": {
            "versao_app": "1.0.0",
            "ambiente": "teste"
        }
    }

def test_registro_auditoria_modelo(registro_exemplo):
    """Testa a criação de um modelo de registro de auditoria."""
    registro = RegistroAuditoria(**registro_exemplo)
    
    assert registro.tipo_operacao == TipoOperacao.LEITURA
    assert registro.nivel_sensibilidade == NivelSensibilidade.ALTO
    assert registro.usuario_id == "user123"
    assert registro.recurso == "teste_psicologico"
    assert registro.detalhes["teste_id"] == "test123"
    assert registro.ip_address == "192.168.1.1"
    assert registro.user_agent == "Mozilla/5.0"
    assert registro.metadata["versao_app"] == "1.0.0"
    assert registro.status == "sucesso"
    assert registro.erro is None

def test_registrar_operacao(audit_manager, registro_exemplo):
    """Testa o registro de uma operação."""
    registro = audit_manager.registrar_operacao(**registro_exemplo)
    
    assert isinstance(registro, RegistroAuditoria)
    assert registro.timestamp is not None
    assert registro.tipo_operacao == registro_exemplo["tipo_operacao"]
    assert registro.nivel_sensibilidade == registro_exemplo["nivel_sensibilidade"]
    assert registro.usuario_id == registro_exemplo["usuario_id"]
    assert registro.recurso == registro_exemplo["recurso"]
    assert registro.detalhes == registro_exemplo["detalhes"]
    assert registro.ip_address == registro_exemplo["ip_address"]
    assert registro.user_agent == registro_exemplo["user_agent"]
    assert registro.metadata == registro_exemplo["metadata"]

def test_registrar_erro(audit_manager, registro_exemplo):
    """Testa o registro de um erro em uma operação."""
    registro = audit_manager.registrar_operacao(**registro_exemplo)
    erro = "Erro ao acessar recurso"
    
    audit_manager.registrar_erro(registro, erro)
    
    assert registro.status == "erro"
    assert registro.erro == erro

def test_registrar_operacao_invalida(audit_manager):
    """Testa o registro de uma operação com dados inválidos."""
    with pytest.raises(ValueError):
        audit_manager.registrar_operacao(
            tipo_operacao="tipo_invalido",  # Tipo inválido
            nivel_sensibilidade=NivelSensibilidade.ALTO,
            usuario_id="user123",
            recurso="teste",
            detalhes={}
        )

def test_registrar_operacao_minima(audit_manager):
    """Testa o registro de uma operação com dados mínimos."""
    registro = audit_manager.registrar_operacao(
        tipo_operacao=TipoOperacao.LEITURA,
        nivel_sensibilidade=NivelSensibilidade.BAIXO,
        usuario_id="user123",
        recurso="teste",
        detalhes={}
    )
    
    assert isinstance(registro, RegistroAuditoria)
    assert registro.timestamp is not None
    assert registro.ip_address is None
    assert registro.user_agent is None
    assert registro.metadata is None

def test_consultar_registros_nao_implementado(audit_manager):
    """Testa que a consulta de registros ainda não está implementada."""
    with pytest.raises(NotImplementedError):
        audit_manager.consultar_registros(
            filtros={},
            periodo_inicio=datetime.now(),
            periodo_fim=datetime.now()
        )

def test_exportar_registros_nao_implementado(audit_manager):
    """Testa que a exportação de registros ainda não está implementada."""
    with pytest.raises(NotImplementedError):
        audit_manager.exportar_registros(
            periodo_inicio=datetime.now(),
            periodo_fim=datetime.now(),
            formato="json"
        )

def test_limpar_registros_antigos_nao_implementado(audit_manager):
    """Testa que a limpeza de registros antigos ainda não está implementada."""
    with pytest.raises(NotImplementedError):
        audit_manager.limpar_registros_antigos(dias=365)

def test_log_file_creation(audit_manager, registro_exemplo):
    """Testa a criação do arquivo de log."""
    # Registra uma operação
    audit_manager.registrar_operacao(**registro_exemplo)
    
    # Verifica se o arquivo de log foi criado
    assert os.path.exists("logs/audit.log")
    
    # Lê o conteúdo do arquivo
    with open("logs/audit.log", "r") as f:
        log_content = f.read()
    
    # Verifica se o conteúdo do log contém as informações esperadas
    assert "user123" in log_content
    assert "WAIS-IV" in log_content
    assert "192.168.1.1" in log_content
    assert "Mozilla/5.0" in log_content

def test_registro_auditoria_serialization(registro_exemplo):
    """Testa a serialização do registro de auditoria."""
    registro = RegistroAuditoria(**registro_exemplo)
    
    # Converte para JSON
    json_data = registro.json()
    
    # Verifica se o JSON contém todos os campos necessários
    data = json.loads(json_data)
    assert "timestamp" in data
    assert data["tipo_operacao"] == "leitura"
    assert data["nivel_sensibilidade"] == "alto"
    assert data["usuario_id"] == "user123"
    assert data["recurso"] == "teste_psicologico"
    assert "teste_id" in data["detalhes"]
    assert data["ip_address"] == "192.168.1.1"
    assert data["user_agent"] == "Mozilla/5.0"
    assert data["status"] == "sucesso"
    assert data["erro"] is None
    assert "versao_app" in data["metadata"] 