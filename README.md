## terminal
This is [celery-tasks](https://superset.incubator.apache.org/installation.html#celery-tasks "Title")

```docker exec superset bash```

```celery worker --app=superset.tasks.celery_app:app --pool=prefork -O fair -c 4 -E```

with 4 is core number in your server

## in another terminal

```docker exec superset bash```

```celery beat --app=superset.tasks.celery_app:app```

## to check redis db
```redis-cli -a jFMPDBU5A2zhXEC5```

```INFO keyspace```

```select 0```

```KEYS *```

```MGET {key}```