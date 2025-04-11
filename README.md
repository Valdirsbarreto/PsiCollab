# PsiCollab

Sistema de assistência na elaboração de laudos psicológicos utilizando IA.

## 🚀 Funcionalidades

- Autenticação via Google OAuth2
- Autenticação via SMS (Twilio Verify)
- Dashboard interativo
- Sistema de cache com Redis
- Busca semântica com Qdrant
- Interface moderna e responsiva

## 🛠️ Tecnologias

- Python 3.9+
- FastAPI
- Redis
- Qdrant
- Docker & Docker Compose
- Twilio Verify API
- Google OAuth2

## 📋 Pré-requisitos

- Docker e Docker Compose
- Conta Twilio (para autenticação SMS)
- Projeto Google Cloud (para OAuth2)
- Python 3.9 ou superior (para desenvolvimento local)

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/psicollab.git
cd psicollab
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

3. Inicie os containers:
```bash
docker-compose up -d
```

4. Acesse a aplicação:
```
http://localhost:8080
```

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` com as seguintes variáveis:

```env
# Google OAuth2
GOOGLE_CLIENT_ID=seu_client_id
GOOGLE_CLIENT_SECRET=seu_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8080/api/auth/google/callback

# Twilio
TWILIO_ACCOUNT_SID=seu_account_sid
TWILIO_AUTH_TOKEN=seu_auth_token
TWILIO_VERIFY_SID=seu_verify_sid

# JWT
JWT_SECRET_KEY=sua_chave_secreta

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
```

## 📦 Estrutura do Projeto

```
psicollab/
├── app/
│   ├── core/
│   │   └── sms_auth.py
│   ├── static/
│   │   └── js/
│   │       └── auth.js
│   └── templates/
│       ├── auth.html
│       └── dashboard.html
├── docker/
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── psicollab_app.py
└── requirements.txt
```

## 👥 Contribuição

1. Faça o fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## ✨ Próximos Passos

- [ ] Implementar interface principal do dashboard
- [ ] Desenvolver sistema de criação de laudos
- [ ] Integrar com Qdrant para busca semântica
- [ ] Adicionar gerenciamento de pacientes
- [ ] Implementar templates de laudos