# Use a imagem oficial do Python como base
FROM python:3.8-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para dentro do contêiner
COPY requirements.txt /app/

# Instale as dependências do Flask
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o código da aplicação para o contêiner
COPY . /app/

# Exponha a porta em que o Flask estará rodando
EXPOSE 5000

# Comando para rodar o app Flask
CMD ["python", "app.py"]