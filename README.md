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
#### Диаграмма развертывания представлена на рисунке
![Alt-текст](https://github.com/Pav9551/aio_test_bot/blob/main/tg_bot_deployment.png "Deployment")

## Перед сборкой контейнеров необходимо
- Скопировать файлы:
```
git clone https://github.com/Pav9551/aio_test_bot
```


- Установить токен Ваш токен TG в ./bot/__main__:
```
BOT_TOKEN = '5242****:AAHRf******jIJ7QY3s'

host = '**.***.***.***'
```
- Создать файл виртуального окружения;
```
nano .env
SQLALCHEMY_WARN_20=1
POSTGRES_DATABASE= postgres
POSTGRES_USER= email
POSTGRES_PASSWORD= password
POSTGRES_PORT= 5432
POSTGRES_HOST= db
PG_DATA = /var/lib/pgsql/pgdata
LOGGING_LEVEL=1
PGADMIN_DEFAULT_EMAIL = email@ya.ru
PGADMIN_DEFAULT_PASSWORD = password

```
## Сборка контейнеров

 - содержимое скрипта restart
```curl
docker-compose down
docker-compose build
docker-compose up -d 
```
 - сделать файл restart.sh исполняемым:
```curl 
 sudo chmod +x restart
 ```
 - Собрать и запустить контейнеры скриптом ./restart.sh

 - и проверить их работу
```curl
docker-compose ps
```

- Установить права на папку если необходимо:
```
 sudo chown -R 5050:5050 pgadmin

 - для добавления пользователя в базу данных сделайте запрос (воспользуйтесь pgadmin http://***.***.***.***:8080/)
```curl
INSERT INTO Users (id, username, email, age) VALUES (1,'newuser1', 'newuser@example.com', 28)
```


```
<a name="myfootnote1">1</a> Информация по установке сервисов docker и docker-compose взята с сайта https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04-ru и https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04 (step1)
```
```
<a name="myfootnote2">2</a> Информация по работе с API для nocodb взята с сайта https://apis.nocodb.com/ и https://giters.com/elchicodepython/python-nocodb:
