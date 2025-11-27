# Usa uma imagem oficial de Python
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos do projeto para dentro do container
COPY . /app

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Comando para rodar a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
