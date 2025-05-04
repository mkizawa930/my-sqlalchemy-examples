# README.md


## MEMO

### SQLAlchemy

**DBの作成**

```python
# sqlite3
DATABASE_URL = "sqlite:///:memory:"

# postgres
DATABASE_URL = "postgresql://{username}:{password}@{hostname}:{port}/{dbname}"

# mysql
DATABASE_URL = "mysql://"
```


## Examples


### SNS


```bash
# テストの実行
PYTHONPATH=./examples/sns uv run pytest -s ./examples/sns/tests
```