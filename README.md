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