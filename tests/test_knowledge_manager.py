"""
Testes para o gerenciador da base de conhecimento.
"""
import pytest
import json
import os
from datetime import datetime
from unittest.mock import Mock, patch, AsyncMock
from app.core.knowledge_manager import KnowledgeManager

@pytest.fixture
def knowledge_manager(tmp_path):
    """Cria uma instância do KnowledgeManager para testes."""
    with patch('app.core.config.settings') as mock_settings:
        mock_settings.KNOWLEDGE_BASE_DIR = str(tmp_path)
        return KnowledgeManager()

@pytest.fixture
def documento_exemplo():
    """Cria um documento de exemplo para testes."""
    return {
        "id": "doc_001",
        "tipo": "teste",
        "conteudo": "Este é um texto de exemplo para teste.",
        "metadata": {
            "fonte": "Manual de Testes",
            "ano": 2024,
            "relevancia": "alta",
            "autor": "Teste"
        }
    }

@pytest.mark.asyncio
async def test_inicializar_base_conhecimento_vazio(knowledge_manager):
    """Testa a inicialização da base de conhecimento vazia."""
    resultado = await knowledge_manager.inicializar_base_conhecimento()
    
    assert resultado["status"] == "aviso"
    assert resultado["mensagem"] == "Nenhum arquivo JSON encontrado"
    assert resultado["arquivos_processados"] == 0
    assert resultado["total_documentos"] == 0
    assert resultado["documentos_processados"] == 0

@pytest.mark.asyncio
async def test_inicializar_base_conhecimento_com_arquivos(knowledge_manager, documento_exemplo):
    """Testa a inicialização da base de conhecimento com arquivos."""
    # Cria um arquivo JSON de exemplo
    arquivo_json = os.path.join(knowledge_manager.knowledge_dir, "teste.json")
    with open(arquivo_json, "w", encoding="utf-8") as f:
        json.dump([documento_exemplo], f)
    
    # Mock do processamento de arquivo
    with patch.object(knowledge_manager.embedding_generator, "processar_arquivo_json", 
                     return_value=(1, 1)):
        resultado = await knowledge_manager.inicializar_base_conhecimento()
        
        assert resultado["status"] == "sucesso"
        assert resultado["arquivos_processados"] == 1
        assert resultado["total_documentos"] == 1
        assert resultado["documentos_processados"] == 1
        assert resultado["taxa_sucesso"] == "100.00%"

@pytest.mark.asyncio
async def test_adicionar_documento(knowledge_manager, documento_exemplo):
    """Testa a adição de um novo documento."""
    # Mock do processamento de documento
    documento_processado = {
        **documento_exemplo,
        "embedding": [0.1, 0.2, 0.3],
        "data_processamento": datetime.now().isoformat()
    }
    
    with patch.object(knowledge_manager.embedding_generator, "processar_documento",
                     return_value=documento_processado), \
         patch.object(knowledge_manager.embedding_generator, "armazenar_na_vector_db",
                     return_value=True):
        
        resultado = await knowledge_manager.adicionar_documento(documento_exemplo)
        
        assert resultado is True
        
        # Verifica se o arquivo JSON foi criado
        arquivo_json = os.path.join(knowledge_manager.knowledge_dir, "teste.json")
        assert os.path.exists(arquivo_json)
        
        # Verifica o conteúdo do arquivo
        with open(arquivo_json, "r", encoding="utf-8") as f:
            documentos = json.load(f)
            assert len(documentos) == 1
            assert documentos[0]["id"] == documento_exemplo["id"]

@pytest.mark.asyncio
async def test_adicionar_documento_erro(knowledge_manager, documento_exemplo):
    """Testa o tratamento de erro na adição de documento."""
    # Mock do processamento de documento com erro
    with patch.object(knowledge_manager.embedding_generator, "processar_documento",
                     side_effect=Exception("Erro de processamento")):
        
        resultado = await knowledge_manager.adicionar_documento(documento_exemplo)
        
        assert resultado is False

@pytest.mark.asyncio
async def test_criar_base_conhecimento_inicial(knowledge_manager):
    """Testa a criação da base de conhecimento inicial."""
    # Mock da criação de arquivos de exemplo
    with patch.object(knowledge_manager, "_criar_arquivo_exemplo"), \
         patch.object(knowledge_manager, "inicializar_base_conhecimento",
                     return_value={
                         "status": "sucesso",
                         "arquivos_processados": 9,
                         "total_documentos": 18,
                         "documentos_processados": 18,
                         "taxa_sucesso": "100.00%"
                     }):
        
        resultado = await knowledge_manager.criar_base_conhecimento_inicial()
        
        assert resultado["status"] == "sucesso"
        assert resultado["arquivos_processados"] == 9
        assert resultado["total_documentos"] == 18
        assert resultado["documentos_processados"] == 18
        assert resultado["taxa_sucesso"] == "100.00%"

@pytest.mark.asyncio
async def test_criar_base_conhecimento_inicial_erro(knowledge_manager):
    """Testa o tratamento de erro na criação da base de conhecimento inicial."""
    # Mock da criação de arquivos de exemplo com erro
    with patch.object(knowledge_manager, "_criar_arquivo_exemplo",
                     side_effect=Exception("Erro na criação")):
        
        resultado = await knowledge_manager.criar_base_conhecimento_inicial()
        
        assert resultado["status"] == "erro"
        assert "mensagem" in resultado

def test_gerar_documentos_exemplo_wechsler(knowledge_manager):
    """Testa a geração de documentos de exemplo para a categoria wechsler."""
    documentos = knowledge_manager._gerar_documentos_exemplo("wechsler")
    
    assert len(documentos) == 2
    assert documentos[0]["id"] == "wechsler_001"
    assert documentos[1]["id"] == "wechsler_002"
    assert all(doc["tipo"] == "wechsler" for doc in documentos)

def test_gerar_documentos_exemplo_personalidade(knowledge_manager):
    """Testa a geração de documentos de exemplo para a categoria personalidade."""
    documentos = knowledge_manager._gerar_documentos_exemplo("personalidade")
    
    assert len(documentos) == 2
    assert documentos[0]["id"] == "personalidade_001"
    assert documentos[1]["id"] == "personalidade_002"
    assert all(doc["tipo"] == "personalidade" for doc in documentos)

def test_gerar_documentos_exemplo_atencao(knowledge_manager):
    """Testa a geração de documentos de exemplo para a categoria atenção."""
    documentos = knowledge_manager._gerar_documentos_exemplo("atencao")
    
    assert len(documentos) == 2
    assert documentos[0]["id"] == "atencao_001"
    assert documentos[1]["id"] == "atencao_002"
    assert all(doc["tipo"] == "atencao" for doc in documentos)

def test_gerar_documentos_exemplo_normativas(knowledge_manager):
    """Testa a geração de documentos de exemplo para a categoria normativas."""
    documentos = knowledge_manager._gerar_documentos_exemplo("normativas")
    
    assert len(documentos) == 2
    assert documentos[0]["id"] == "normativas_001"
    assert documentos[1]["id"] == "normativas_002"
    assert all(doc["tipo"] == "normativas" for doc in documentos)

def test_gerar_documentos_exemplo_etica(knowledge_manager):
    """Testa a geração de documentos de exemplo para a categoria ética."""
    documentos = knowledge_manager._gerar_documentos_exemplo("etica")
    
    assert len(documentos) == 2
    assert documentos[0]["id"] == "etica_001"
    assert documentos[1]["id"] == "etica_002"
    assert all(doc["tipo"] == "etica" for doc in documentos)

def test_gerar_documentos_exemplo_categoria_desconhecida(knowledge_manager):
    """Testa a geração de documentos de exemplo para uma categoria desconhecida."""
    documentos = knowledge_manager._gerar_documentos_exemplo("categoria_desconhecida")
    
    assert len(documentos) == 0 