# Sdo parser
API для просмотра заполненности курсов [СЭДО СВФУ](https://sdo.s-vfu.ru/)

## Использование
Для запуска приложения нужно сделать следующие шаги:

Запустите командную строку и склонируйте репозиторий с помощью команды:
```sh
$ git clone https://github.com/sqrtleet/sdo-api.git
```
Откройте папку с проектом в командной строке и создайте виртуальное окружение:
```sh
$ py -m venv venv
```
Потом активируйте ее:
```sh
$ .\venv\Scripts\activate
```
Установите инструмент для управления зависимостями:
```sh
$ pip install poetry
```
Установаите все необходимые зависимости:
```sh
$ poetry install
```
Запустите сервер:
```sh
$ py main.py
```
Теперь вы можете перейти по [адресу](http://127.0.0.1:8000/) для работы с API.