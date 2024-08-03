# Use a imagem oficial do Node.js como base
FROM node:14

# Cria um diretório de trabalho
WORKDIR /usr/src/app

# Copia o package.json e o package-lock.json
COPY package*.json ./

# Instala as dependências
RUN npm install

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta que a aplicação vai usar
EXPOSE 8080

# Define o comando para iniciar a aplicação
CMD [ "npm", "start" ]