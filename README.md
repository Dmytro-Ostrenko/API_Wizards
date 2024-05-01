#  <p align="center">:robot:  API_Wizards:robot:  </p>     
# <p align="center">*Інструкція з встановлення та користування  застосунком “PhotoShare” (REST API)*</p>
## Передумови

Переконайтеся, що на вашому комп'ютері встановлено Python версії 3.11 або новіше. Ви можете завантажити Python з [офіційного сайту](https://www.python.org/downloads/).

## Встановлення

Перед тим, як ви почнете використовувати застосунк “PhotoShare”, вам потрібно встановити його. Дотримуйтесь цих кроків:

1. Клонуйте репозиторій на свій комп'ютер :white_check_mark::    

```
git clone https://github.com/Dmytro-Ostrenko/API_Wizards
```

2. Перейдіть в каталог проєкту :white_check_mark::    

```
cd API_Wizards
```



4. Встановіть “PhotoShare”  як Python-пакет :white_check_mark::
```
pip install . 
```

5. Далі встановлюємо poetry (віртуальне оточення) :white_check_mark::
```
pip install poetry 
```

6. Оновлюємо залежності встановленних бібліотек :white_check_mark::
```
poetry pdate
```

7. Та активуємо віртуальне середовище :white_check_mark::
```
poetry shell
```

Через те, що в проекті є вже створенна БД (яка знаходиться у migrations/versions), крок із її створення пропускаємо за це відповідає команда:
```
alembic revision --autogenerate -m 'Init'
```
## Налаштування та з'єднання із БД
Для початку роботи із БД переконайтесь, що у Вас встановлено та оновлені до останньої версії наступні програми:

* DockerDesktop (посилання для завантаження: https://www.docker.com/products/docker-desktop/)
* DBeaver (посилання для завантаження: https://dbeaver.io/download/)

Після відкриття програм  DBeaver та DockerDesktop, спершу налаштуємо з'єднання та запустимо контейнер у DockerDesktop, для цього вже було створено файл docker-compose.yml :white_check_mark: для цього виконуємо команду:
```
docker compose up -d
```
Вірн налаштування з'єднання у DBeaver потребує вказати значення: 
- name DB
- user
- password
- ports

Після вірного налаштування виконуємо команду для оновлення БД :white_check_mark::
```
alembic upgrade head
```

І нарешті після цього для запуску fastapi виконуємо команду :white_check_mark::
```
uvicorn main:app --reload   
``` 
І за адресою : http://127.0.0.1:8000 стає доступним застосунок :robot: “PhotoShare” :robot:   А за http://127.0.0.1:8000/docs Swagger – розумна документація “PhotoShare”


### Робота із застосунком “PhotoShare” 


### Назви фільтрів для обробки зображень в Cloudinary та їх функції:

- grayscale: Перетворює зображення в чорно-біле.
- sepia: Додає ефект старовинності до зображення.
- blackwhite: Перетворює зображення в чорно-біле з високим контрастом.
- saturation: Контролює насиченість кольорів на зображенні.
- brightness: Регулює яскравість зображення.
- contrast: Контролює контрастність між кольорами на зображенні.
- blur: Розмиває зображення, створюючи ефект розфокусування.
- sharpen: Підвищує різкість зображення.
- hue: Змінює тон кольору на зображенні.
- invert: Інвертує кольори на зображенні.
