# mlops_hw

### Перед запуском надо:
- установить зависимости:
``` shell 
poetry install
```
- накатить миграции на базу через alembic:

```shell
cd src
alembic revision --autogenerate
alembic upgrade head  
```

### Запуск:

```shell
make run-app
```