# Check app

## Запуск
1. Створити env файл
2. Створити БД і заповнити env файл
3. Запуск команди
```bash
export CHECK_ENV=/path/to/file/.env  
```
3. Запуск команди
```bash
uvicorn src.main:app --reload 
```

## Допрацювання
1. Використання Docker
2. Використання CI/CD(Github Actions)
