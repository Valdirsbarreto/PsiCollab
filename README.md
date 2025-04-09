# PsiCollab

Sistema avançado de assistência na elaboração de laudos psicológicos.

## 🚀 Características

- Autenticação segura via Google OAuth2
- Interface moderna e responsiva
- Acesso exclusivo para profissionais de psicologia
- Conformidade com LGPD

## 🛠️ Tecnologias

- Python 3.9+
- FastAPI
- Docker
- OAuth2 (Google)

## 📋 Pré-requisitos

- Docker Desktop
- Git
- Credenciais do Google OAuth2

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/psicollab.git
cd psicollab
```

2. Configure as variáveis de ambiente:
Crie um arquivo `.env` com:
```env
GOOGLE_CLIENT_ID=seu_client_id
GOOGLE_CLIENT_SECRET=seu_client_secret
```

3. Build e execute com Docker:
```bash
docker build -t psicollab .
docker run -p 8080:8080 psicollab
```

## 🚀 Uso

1. Acesse http://localhost:8080
2. Faça login com sua conta Google
3. Acesse as funcionalidades disponíveis

## 🔐 Segurança

- Autenticação OAuth2
- Tokens JWT
- HTTPS (em produção)
- Conformidade LGPD

## 📄 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes.

## ✨ Contribuição

1. Faça o fork do projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request