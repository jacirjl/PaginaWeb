# Use uma imagem base do Python
FROM python:3.9-slim-buster

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos do projeto para o contêiner
COPY . /app

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Defina a variável de ambiente para o Flask
ENV FLASK_APP=app.py

# Exponha a porta 5000
EXPOSE 5000

# Comando para executar o aplicativo
CMD ["flask", "run", "--host=0.0.0.0"]
