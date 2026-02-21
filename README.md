# 🛒 ZLAGODA — Backend (API)

АІС для регулювання роботи продуктового міні-супермаркету. Побудовано з використанням архітектури 3 ярусної архітектури

## 🛠 Технологічний стек
- **Framework:** Django 6.0 (DRF)
- **Database:** PostgreSQL 17
- **Documentation:** Swagger (drf-spectacular)
- **Containerization:** Docker

## 🚀 Швидкий запуск
1. **Налаштування оточення**: Скопіюйте `.env.example` та перейменуйте у `.env` та заповніть усі поля
2. **Збірка та запуск**: 
    ```bash
    docker-compose build
    docker-compose up -d
    ```
   
## 📍 Ендпоінти
 - **Swagger UI**: http://localhost:8000/api/docs/ — основне місце для тестування API.
 - **Admin Panel**: http://localhost:8000/admin/

## 🏗 Архітектура
 - `repositories/`: Raw SQL запити до бази даних. 
 - `services/`: Бізнес-логіка та валідація. 
 - `views/`: Обробка HTTP запитів та документація Swagger.