# Estágio de build
FROM python:3.9-slim as builder

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias para build
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Cria e ativa ambiente virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiar os arquivos de requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Estágio final
FROM python:3.9-slim

# Instala curl para healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copia o ambiente virtual do estágio de build
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Define o diretório de trabalho
WORKDIR /app

# Criar diretórios necessários
RUN mkdir -p /app/app/static /app/app/data /app/app/templates

# Copiar o código da aplicação
COPY app /app/app/
COPY psicollab_app.py /app/
COPY requirements.txt /app/

# Define as variáveis de ambiente
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    HOST=0.0.0.0

# Expor a porta que a aplicação usa
EXPOSE 8080

# Usuário não-root para segurança
RUN useradd -m appuser && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app/app/static
USER appuser

# Healthcheck para monitoramento
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Comando para executar a aplicação
CMD ["uvicorn", "psicollab_app:app", "--host", "0.0.0.0", "--port", "8080", "--reload"] 