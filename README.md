# PsiCollab

Sistema avançado de inteligência artificial para auxiliar psicólogos na elaboração de laudos psicológicos.

## Visão Geral

O PsiCollab é um sistema avançado de inteligência artificial projetado exclusivamente para auxiliar psicólogos na elaboração de laudos psicológicos a partir da análise de testes padronizados. Atuando como um copiloto inteligente, o sistema analisa resultados de avaliações, dialoga com o profissional e contribui para a elaboração de documentos técnicos precisos, em conformidade com as normativas do Conselho Federal de Psicologia.

O sistema se destaca por sua abordagem inequivocamente centrada no profissional, onde a IA nunca substitui o julgamento clínico do psicólogo, mas potencializa suas capacidades interpretativas e reduz significativamente o tempo dedicado à documentação. Isso permite maior foco na relação terapêutica, resultando em benefícios tanto para o profissional quanto para o paciente.

Todas as interações com o sistema são exclusivas para profissionais qualificados, preservando e fortalecendo a relação psicólogo-paciente. A arquitetura do sistema foi projetada com foco em segurança, privacidade e conformidade com a LGPD e outras regulamentações pertinentes.

## Status Atual do Projeto

**Status:** Fase 1 - MVP em desenvolvimento (Março 2024)

### Funcionalidades Implementadas:
- ✅ Estruturação da base de conhecimento com documentos de exemplo
- ✅ Processamento de documentos e geração de embeddings via OpenAI
- ✅ Armazenamento vetorial usando Qdrant
- ✅ Sistema de inicialização da base de conhecimento

### Próximos Passos:
1. Implementação do sistema de busca semântica
2. Desenvolvimento de endpoints de consulta
3. Criação da interface de usuário
4. Integração com o sistema de autenticação

## Principais Características

- Assistente de IA especializado para interpretação de testes psicológicos padronizados
- Processamento avançado de diversos tipos de testes (cognitivos, personalidade, projetivos, etc.)
- Interface conversacional para diálogo natural com o psicólogo
- Editor colaborativo para elaboração assistida de laudos
- Sistema de templates em conformidade com a Resolução CFP nº 06/2019
- Segurança e privacidade com criptografia de ponta a ponta e controle rigoroso de acesso
- Compartilhamento controlado via sistema de QR Code para médicos e outros profissionais
- Armazenamento seguro em banco de dados criptografado para consultas futuras

## Tecnologias Utilizadas

- **Linguagem Principal:** Python 3.11+
- **Frameworks e Bibliotecas:**
  - OpenAI API (geração de embeddings)
  - Qdrant (banco de dados vetorial)
  - FastAPI (framework web)
  - Pydantic (validação de dados)
  - aiohttp (requisições assíncronas)
- **Infraestrutura:**
  - Docker (containers)
  - PostgreSQL (armazenamento relacional)
  - Qdrant (armazenamento de vetores)

### Arquitetura Simplificada
```
                   ┌─────────────┐
                   │   Cliente   │
                   └──────┬──────┘
                          │
                          ▼
┌────────────────────────────────────────┐
│               API REST                 │
└───────────────────┬────────────────────┘
                    │
       ┌────────────┴────────────┐
       │                         │
       ▼                         ▼
┌─────────────┐         ┌─────────────────┐
│  RAG Engine │◄────────┤ Knowledge Base  │
└──────┬──────┘         └─────────┬───────┘
       │                          │
       ▼                          ▼
┌─────────────┐         ┌─────────────────┐
│  OpenAI API │         │     Qdrant      │
└─────────────┘         └─────────────────┘
```

## Instalação e Execução

### Pré-requisitos
- Python 3.11 ou superior
- Docker Desktop
- Chave de API da OpenAI

### Configuração do Ambiente

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Valdirsbarreto/PsiCollab.git
   cd PsiCollab
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
   ```
   OPENAI_API_KEY=sua_chave_api_aqui
   ```

4. **Inicie o Qdrant:**
   ```bash
   docker run -d -p 6333:6333 -p 6334:6334 qdrant/qdrant
   ```

5. **Inicialize a base de conhecimento:**
   ```bash
   python -m app.scripts.initialize_knowledge_base --mode=initialize
   ```

## Estrutura de Arquivos

```
PsiCollab/
├── app/                    # Código principal da aplicação
│   ├── core/               # Componentes centrais
│   │   ├── knowledge_manager.py  # Gerenciador da base de conhecimento
│   │   ├── embedding_generator.py # Gerador de embeddings
│   │   └── ...
│   ├── scripts/            # Scripts utilitários
│   └── ...
├── data/                   # Dados do sistema
│   └── knowledge_base/     # Arquivos JSON de conhecimento
├── docs/                   # Documentação
│   └── PROGRESSO.md        # Registro de progresso do projeto
└── requirements.txt        # Dependências do projeto
```

## Fases de Desenvolvimento
O projeto será desenvolvido em três fases principais:

1. **Fase 1: MVP (3-4 meses)** - Implementação das funcionalidades essenciais para demonstrar o valor central da proposta
2. **Fase 2: Expansão (6 meses)** - Ampliação das capacidades com suporte a testes projetivos e sistema de QR Code
3. **Fase 3: Especialização (8 meses)** - Módulos avançados para áreas específicas e integração com sistemas externos

## Contribuição

Contribuições são bem-vindas! Se você deseja contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Padrões de Código
- Siga o padrão PEP 8 para código Python
- Documente funções e classes usando docstrings
- Escreva testes para novas funcionalidades

## Licença e Autoria

**Autoria:** Valdir Barreto

**Licença:** Todos os direitos reservados. Este software é proprietário e seu uso, distribuição ou modificação não autorizada é estritamente proibida.

---

© 2024 PsiCollab - Sistema de Assistência para Laudos Psicológicos