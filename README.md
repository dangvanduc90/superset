## terminal
```docker exec superset bash```

```celery worker --app=superset.tasks.celery_app:app --pool=prefork -O fair -c 4 -E```

## in another terminal

```docker exec superset bash```

```celery beat --app=superset.tasks.celery_app:app```