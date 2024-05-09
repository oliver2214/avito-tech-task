# Описание проекта

## Техническое задание на стажировку в Авито.

**Задание заключалось в написании микросервиса на языке Python(FastAPI)**

Структура БД: 

Tags - o2m - Banners - m2m - Features

Есть 3 сущности: баннеры, теги, фичи. Фича содержит много баннеров, баннеры могут содержать много тегов, один тег может содержаться в нескольких баннерах. То есть 2 связи между таблицами: многие ко многим(баннеры и теги) и один ко многим(фича и баннеры). 

**Трудности с которыми я столкнулся:**
* Были написаны следующие эндпоинты: get(по фича-тег), get(все баннеры по фильтру), post(баннера), patch(изменение баннера), delete(удаление баннера). (FastAPI)
* Сочетание фича-тег однозначно определяют баннер. Поэтому необходимо было построить сложный запрос при помощи ORM с двумя join'ами, минуя проблему N+1. (sqlalchemy, alembic)
* Юнит-тесты и интеграционный(pytest)
* Кэширование(redis)
* Docker, docker-compose

**Технологии:**
Python • FastAPI • PostgreSQL • SQLalchemy • Тестирование API • Git • SQL • Docker • Redis

# Инструкция по запуску приложения

## Подготовка окружения

1. Установите Docker и Docker Compose, если они еще не установлены.

## Запуск приложения через docker-compose

1. Склонируйте репозиторий:
   `git clone git@github.com:oliver2214/avito-tech-task.git`

2. Перейдите в каталог с проектом:
   `cd avito-tech-task`

3. Соберите образ приложения с помощью команды:
   `docker build .`

4. Запустите приложение с помощью Docker Compose:
   `docker compose up`

   *Если с первого раза не получится повторите команду*

6. Приложение будет доступно по адресу [localhost:7777](http://localhost:7777).

7. Документация по API будет доступна по адресу [localhost:7777/docs](http://localhost:7777/docs).

## Вопросы, с которыми столкнулся

**При создании новых баннеров, неизвестно есть ли данные в базе данных, включая таблицы с тегами и фичами.**

**Если база данных пуста, добавление нового баннера становится невозможным из-за нарушения ограничений внешних ключей, которые связаны с тегами и фичами баннера.**

**Мое решение:**

При добавлении нового баннера:

- В базу данных добавляются все теги, содержащиеся в данном баннере, если их еще нет в базе.
- В базу данных добавляется фича, к которой привязан баннер, если ее еще нет в базе.
- После этого добавляется баннер и создаются связи.
