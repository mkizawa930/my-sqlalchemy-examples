# README.md


## DBの作成

```python
# sqlite3
DATABASE_URL = "sqlite:///:memory:"

# postgres
DATABASE_URL = "postgresql://{username}:{password}@{hostname}:{port}/{dbname}"

# mysql
DATABASE_URL = "mysql://"
```