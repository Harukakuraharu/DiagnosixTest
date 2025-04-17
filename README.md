# Микросервис Diagnosix — auth-service

## Запуск приложения
Для начала, необходимо скачать репозиторий локально к себе на устройство
```
git clone git@github.com:Harukakuraharu/DiagnosixTest.git
```
После этого, в корневой директории необходимо создать файл *.env*, пример лежит в файле [env.example](https://github.com/Harukakuraharu/DiagnosixTest/blob/main/.env.example).

## Команда для сборки и запуска приложения
```
docker compose up --build -d
```
Приложение доступно по адресу: **http://127.0.0.1:80/docs/**


## Дополнительные команды
Если есть необходимость перезапустить определенные контейнеры:
```
docker compose up --build  --no-deps -d имя_контейнера
```
Eсли нужно остановить все контейнеры (флаг -v для удаления всех данных):
```
docker compose down -v
```
Eсли нужно открыть контейнер в консоли
```
docker compose exec имя_контейнера sh
```
Если нужно посмотртеть логи контейнера
```
docker compose logs имя_контейнера
```    

## Локальная разработка и запуск тестов
Если есть необходимость локально запустить микросервис, необходимо опустить **Docker** и следовать дальнейшей инструкции:

1. #### Необходимо создать виртуальное окружение
```
python -m venv .venv
```
Активация виртуальной среды для OC Linux
```
source .venv/bin/activate
```
Активация виртуальной среды для OC Windows
```
venv\Scripts\activate
```
2. #### Далее, нужно установить зависимости:
```
pip install poetry
poetry install
```
3. #### После этого введите команду для поднятия базы данных:
```
docker compose -f docker-compose-db.yaml up --build  
```
3. #### Применение миграций
```
cd app/
alembic upgrade head
```
4. #### Для локального запуска приложения на http://127.0.0.1:8000/docs#/ (swagger):
```
uvicorn app.main:app --reload
```
5. #### Запуск тестов:
```
pytest
```