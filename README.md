# aio_test_bot

## Это инструкция по развертыванию telegram бота на aiogram.

```
```
- Сервис позволяет с помощью telegram бота работать с базой данных;
- В данном случае развернута база данных postgresql;

## Оглавление

1. [Требования к операционной системе](#Требования-к-операционной-системе)
2. [Описание файла docker-compose.yaml](#Описание-файла-docker-compose.yaml)
3. [Установка веб-сервиса](#Установка-веб-сервиса)
4. [Пример использования](#Пример-использования)

## Требования к операционной системе
Тестирование сервиса проводилось на операционной системе ubuntu 20.04 установленной на виртуальном выделенном сервере. Перед началом работы необходимо установить на операционную систему docker и docker-compose<sup>[1](#myfootnote1)</sup>
## Описание файла home/docker-compose/docker-compose.yaml

```yaml
version: '3.7'
services:
  db:
    image: postgres:14-alpine
    container_name: db
    restart: always
    volumes:
      - ./db:/var/lib/postgresql
      
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - '5432:5432'
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
  pgadmin:
    image: dpage/pgadmin4
    container_name: pgadmin4
    restart: always
    ports:
      - '8080:80'
    environment:
      - PGADMIN_DEFAULT_EMAIL=${PGADMIN_DEFAULT_EMAIL}
      - PGADMIN_DEFAULT_PASSWORD=${PGADMIN_DEFAULT_PASSWORD}
    volumes:
      - ./pgadmin:/var/lib/pgadmin
    depends_on:
      - db
  bot:
    build: .
    command: sh -c "python -m bot"
    env_file:
      - ./.env
    restart: always
    depends_on:
      - db
volumes:
  pgdata:

```
## Перед сборкой контейнеров необходимо
- Установить права на папку:
```
- sudo chown -R 5050:5050 pgadmin
```
- Установить токен Ваш токен TG в ./bot/__main__:
```
- sudo chown -R 5050:5050 pgadmin
```
- Создать файл виртуального окружения;
```
- nano .env
```

```
POSTGRES_DATABASE= postgres
POSTGRES_USER= email
POSTGRES_PASSWORD= password
PGADMIN_DEFAULT_EMAIL = email@ya.ru
PGADMIN_DEFAULT_PASSWORD = password
```
## Сборка контейнеров

 - содержимое скрипта restart.sh
```curl
docker-compose down
docker-compose build
docker-compose up -d 
```
 - сделать файл restart.sh исполняемым:
```curl 
 sudo chmod +x restart.sh
 ```
 - Собрать и запустить контейнеры скриптом ./restart.sh

 - и проверить их работу
```curl
docker-compose ps
```

 - для добавления пользователя в базу данных сделайте запрос (воспользуйтесь pgadmin http://***.***.***.***:8080/)
```curl
INSERT INTO Users (id, username, email, age) VALUES (1,'newuser1', 'newuser@example.com', 28)
```


```
<a name="myfootnote1">1</a> Информация по установке сервисов docker и docker-compose взята с сайта https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04-ru и https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04 (step1)
```
```
<a name="myfootnote2">2</a> Информация по работе с API для nocodb взята с сайта https://apis.nocodb.com/ и https://giters.com/elchicodepython/python-nocodb:
