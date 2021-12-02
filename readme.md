### steplabs
 

**Запуск проекта**  

- Переход в папку с файлом docker-compose.yml  
```console
cd deploy/steplabs
``` 

- Создание образов  
```console
docker-compose build
```

- Запуск контейнеров  
```console
docker-compose up -d
```

- Применение миграций  
```console
docker-compose exec steplabs_test bash -c "cd db && alembic upgrade head"
```



**Адрес в браузере**  
http://127.0.0.1:8080/docs  
