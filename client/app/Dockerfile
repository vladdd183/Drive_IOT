FROM node

# устанавливаем простой HTTP-сервер для статики
RUN npm install -g http-server

RUN mkdir /diploma

# делаем каталог 'app' текущим рабочим каталогом
WORKDIR /diploma

# копируем оба 'package.json' и 'package-lock.json' (если есть)
COPY package*.json ./


# устанавливаем зависимости проекта
RUN npm install

# копируем файлы и каталоги проекта в текущий рабочий каталог (т.е. в каталог 'app')
COPY . .



# собираем приложение для production с минификацией
# RUN npm run build

# EXPOSE 5173

# EXPOSE 9000
# CMD [ "http-server", "dist" ]

CMD ["npm", "run", "dev", "--host"]

# CMD ["npm", "test:dev"]
# CMD ["npm", "start", "--host", "0.0.0.0:9000"]


