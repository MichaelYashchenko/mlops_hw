# mlops_hw


## Первая домашка

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

### Еще надо добавить для полного счастья:
- Добавить обработку ошибок
- Добавить тайп-хинты, там где их нет
- Добавить докстринги
- Добавить обработку ошибок нормальную
- Добавить логирование (loguru)
- rpc

### Тестировал на датасетах sklearn:
```python
from sklearn import datasets
import pandas as pd


iris = datasets.load_iris()
df = pd.DataFrame(data=iris.data,  
                  columns=iris.feature_names)
df['target'] = iris.target
df.to_json('iris.json', indent=4)
```

## Вторая домашка

Собрал Dockerfile с FastApi и docker-compose c minio, postgres и fast api вместе. Как запускать:
```bash
docker-compose up -d
```
C docker-compose up все работает, но... 
Пытался сбилдить image c помощью **docker-compose build** - получал ошибку, 
что в контейнере не резолвиться host postgres. 
В процессе понял, что docker не умеет
билдить единый контейнер из нескольких, и эта команда только билдит несбилженные 
контейнеры внутри docker-compose.yml. В связи с этим вопрос: что имелось ввиду в пункте:
```
Сборку самого вашего микросервиса в docker образ (образ нужно запушить в docker hub)
```
Какой именно образ здесь имеется ввиду? Образ c Fast Api? Я правильно понимаю, 
что тогда мы как-бы отдельно где-то запускаем minio и postgres, 
и их параметры передаем как переменные окружения для запуска этого образа? 
Потому что, как собрать единый контейнер из docker-compose с несколькими контейнерами я так и не нашел.
Видимо надо уменшить связность.

P.S. Образ я в итоге запушил ([здеся](https://hub.docker.com/repository/docker/myashchenko101/ftiad-mlops/general)), 
но он пока не работает из-за проблем описанных выше.

Хочу фидбек.