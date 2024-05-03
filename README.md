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


## Налаштування та з'єднання із БД
Для початку роботи із БД переконайтесь, що у Вас встановлено та оновлені до останньої версії наступні програми:

* DockerDesktop (посилання для завантаження з [офіційного сайту](https://www.docker.com/products/docker-desktop/).)
* DBeaver (посилання для завантаження:   з [офіційного сайту](https://dbeaver.io/download/).  )

Після відкриття програм  DBeaver та DockerDesktop, спершу налаштуємо з'єднання та запустимо контейнер у DockerDesktop, для цього вже було створено файл docker-compose.yml :white_check_mark: для цього виконуємо команду:
```
docker compose up -d
```
Вірн налаштування з'єднання у DBeaver потребує вказати значення: 
- name DB
- user
- password
- ports

Через те, що в проекті є вже створенна БД (яка знаходиться у migrations/versions), крок із її створення пропускаємо за це відповідає команда:
```
alembic revision --autogenerate -m 'Init'
```

Тому після вірного налаштування виконуємо команду для оновлення БД :white_check_mark::
```
alembic upgrade head
```

І нарешті після цього для запуску fastapi виконуємо команду :white_check_mark::
```
uvicorn main:app --reload   
``` 
І за адресою : http://127.0.0.1:8000 стає доступним застосунок :robot: “PhotoShare” :robot:   А за http://127.0.0.1:8000/docs Swagger – розумна документація “PhotoShare”


## Робота із застосунком “PhotoShare” 

### Авторизація в застосунку:

#### Реєстрація

- **Опис**: Реєстрація нового користувача.
- **Шлях**: `/auth/signup`
- **Метод**: `POST`
-**Вхідні Параметри**:
 - `username`: Нікнейм нового користувача (обов’язкове поле).
 - `email`: Пошта нового користувача (обов’язкове поле).
 - `password`: Пароль (обов’язкове поле).
- **Результат**: Створює у БД нового користувача.

#### Авторизація

- **Опис**: Авторизація існуючого користувача.
- **Шлях**: `/auth/login`
- **Метод**: `POST`
- **Вхідні Параметри**:
 - `email`: Пошта нового користувача (обов’язкове поле).
 - `password`: Пароль (обов’язкове поле).
- **Результат**: Авторизує користувача в системі, визначає його роль та дає відповідний функціонал в застосунку.

#### Зміни ролі користувачів (функція доступна лише адміністраторам)

- **Опис**: Авторизація існуючого користувача.
- **Шлях**: `/auth/change_role`
- **Метод**: `POST`
- **Вхідні Параметри**:
 - `admin_email`: Пошта адміністратора (обов’язкове поле).
 - `admin_email`: Пошта користувача, якому буде змінено роль (обов’язкове поле).
 - `new_role`: Нова роль у БД (обов’язкове поле).
- **Результат**: Змінює роль користувача.

### Керування роботою з фото:

#### Завантаження фото

- **Опис**: Завантаження нового зображення.
- **Шлях**: `/photos/`
- **Метод**: `POST`
- **Вхідні Параметри**:
    - `file`: Файл зображення для завантаження (обов’язкове поле).
- **Результат**: Зображення успішно завантажується у систему.

#### Оновлення опису фото

- **Опис**: Оновлення опису існуючого зображення.
- **Шлях**: `/photos/{photo_id}`
- **Метод**: `PUT`
- **Вхідні Параметри**:
    - `body`: Тіло запиту з новим описом фото.
    - `photo_id`: ID зображення, яке потрібно оновити (обов’язкове поле).
    - `description`: Новий опис для зображення (обов’язкове поле).
- **Результат**: Опис зображення успішно оновлюється.

#### Видалення фото

- **Опис**: Видалення існуючого зображення.
- **Шлях**: `/photos/{photo_id}`
- **Метод**: `DELETE`
- **Вхідні Параметри**:
    - `photo_id`: ID зображення, яке потрібно видалити (обов’язкове поле).
- **Результат**: Зображення успішно видаляється з системи.

#### Отримання інформації про фото

- **Опис**: Отримання інформації про існуюче зображення.
- **Шлях**: `/photos/`
- **Метод**: `GET`
- **Вхідні Параметри**:
    - `url`: URL зображення, для якого потрібно отримати інформацію (обов’язкове поле).
- **Результат**: Інформація про зображення.

#### Зміна розміру фото

- **Опис**: Зміна розміру існуючого зображення.
- **Шлях**: `/photos/resize`
- **Метод**: `POST`
- **Вхідні Параметри**:
    - `url`: URL зображення, яке потрібно змінити розмір (обов’язкове поле).
    - `width`: Нова ширина зображення.
    - `height`: Нова висота зображення.
- **Результат**: Зображення змінює розмір згідно з вказаними параметрами.

#### Обрізка фото

- **Опис**: Обрізка існуючого зображення.
- **Шлях**: `/photos/crop`
- **Метод**: `POST`
- **Вхідні Параметри**:
    - `url`: URL зображення, яке потрібно обрізати (обов’язкове поле).
    - `width`: Ширина нового зображення.
    - `height`: Висота нового зображення.
- **Результат**: Зображення обрізається згідно з вказаними параметрами.

#### Застосування фільтру та тексту до фото

- **Опис**: Застосування фільтру та тексту до існуючого зображення.
- **Шлях**: `/photos/apply-filter-text`
- **Метод**: `POST`
- **Вхідні Параметри**:
    - `url`: URL зображення, до якого потрібно застосувати фільтр та текст (обов’язкове поле).
    - `filter_name`: Назва фільтру, який потрібно застосувати.
    - `text`: Текст, який потрібно додати до зображення.
    - `font_family`: Назва шрифту тексту.
    - `font_size`: Розмір шрифту тексту.
    - `font_color`: Колір шрифту тексту.
- **Результат**: Фільтр та текст успішно застосовуються до зображення.

#### Конвертація формату фото

- **Опис**: Конвертація існуючого зображення в інший формат.
- **Шлях**: `/photos/convert-format`
- **Метод**: `POST`
- **Вхідні Параметри**:
    - `url`: URL зображення, яке потрібно конвертувати (обов’язкове поле).
    - `new_format`: Новий формат зображення.
- **Результат**: Зображення конвертується в новий формат.

#### Отримання метаданих про фото

- **Опис**: Отримання метаданих про існуюче зображення.
- **Шлях**: `/photos/get-metadata`
- **Метод**: `POST`
- **Вхідні Параметри**:
    - `url`: URL зображення, для якого потрібно отримати метадані (обов’язкове поле).
- **Результат**: Метадані про зображення.

#### Отримання посилання на перетворене фото

- **Опис**: Отримання посилання на існуюче перетворене зображення.
- **Шлях**: `/photos/{transformed_photo_id}`
- **Метод**: `GET`
- **Вхідні Параметри**:
    - `transformed_photo_id`: ID перетвореного зображення.
- **Результат**: Посилання на перетворене зображення.

#### Отримання QR-коду для фото

- **Опис**: Генерація QR-коду для існуючого зображення.
- **Шлях**: `/photos/get_qr_code/{transformed_photo_id}/`
- **Метод**: `GET`
- **Вхідні Параметри**:
    - `transformed_photo_id`: ID перетвореного зображення.
- **Результат**: QR-код для зображення.

### Керування коментарями до світлин:

#### Створення коментаря

- **Опис**: Створення нового коментаря до світлини.
- **Шлях**: `/comments/`
- **Метод**: `POST`
- **Вхідні Параметри**:
    - `comment`: Об'єкт коментаря, який містить текст коментаря, ID світлини та ID користувача (обов’язкове поле).
    - `photo_id`: ID світлини, до якої додається коментар (обов’язкове поле).
    - `user_id`: ID користувача, який додає коментар (обов’язкове поле).
- **Результат**: Коментар успішно створюється.

#### Отримання коментарів до світлини

- **Опис**: Отримання коментарів до конкретної світлини.
- **Шлях**: `/comments/{photo_id}/comments`
- **Метод**: `GET`
- **Вхідні Параметри**:
    - `photo_id`: ID світлини, для якої потрібно отримати коментарі (обов’язкове поле).
- **Результат**: Коментарі до світлини.

#### Оновлення коментаря

- **Опис**: Оновлення існуючого коментаря.
- **Шлях**: `/comments/{comment_id}`
- **Метод**: `PUT`
- **Вхідні Параметри**:
    - `comment_id`: ID коментаря, який потрібно оновити (обов’язкове поле).
    - `comment`: Об'єкт коментаря з новим текстом коментаря (обов’язкове поле).
- **Результат**: Коментар успішно оновлюється.

#### Видалення коментаря

- **Опис**: Видалення існуючого коментаря.
- **Шлях**: `/comments/{comment_id}`
- **Метод**: `DELETE`
- **Вхідні Параметри**:
    - `comment_id`: ID коментаря, який потрібно видалити (обов’язкове поле).
- **Результат**: Коментар успішно видаляється.



## Структура проекту застосунку "PhotoShare"

- `main.py`: головний файл програми, що містить маршрути FastAPI.
  - `src/`: каталог, що містить логіку програми;
  - `src/conf/`: каталог, що містить конфігурації програми;
  - `src/database/`: каталог із конфігураціями та моделями бази даних;
  - `src/repository/`: каталог з класами репозиторію для взаємодії з базою даних;
  - `src/routes/`: каталог, що містить модулі маршрутизатора FastAPI;
  - `src/schemas/`: зберігаються схеми даних, які використовуються для валідації та взаємодії з даними в програмному забезпеченні;
  - `src/services/`: зберігаються файли, пов'язані з бізнес-логікою та  функціональністю програмного забезпечення.
- `pyproject.toml`: файл конфігурації Poetry, що містить залежності проекту
- `docker-compose.yml`: файл конфігурації для Docker Compose,  використовується для визначення та налаштування мультиконтейнерних додатків. Файл містить опис сервісів, які складають додаток, а також параметри налаштування контейнерівсередовища Docker.
- `.env`: текстовий файл, який містить змінні середовища для конфігурації для додатку.

## P.S. Додаткова інформація

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
