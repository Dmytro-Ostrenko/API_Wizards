#  <p align="center">:robot:  API_Wizards:robot:  </p>     
# <p align="center"> *:smiley_cat: Мова читання - українська. Інструкція з встановлення та користування  застосунком “PhotoShare” (REST API)*</p>
## Передумови

Переконайтеся, що на вашому комп'ютері встановлено Python версії 3.11 або новіше. Ви можете завантажити Python з [офіційного сайту](https://www.python.org/downloads/).

##  <p align="center">Встановлення</p>     


Перед тим, як ви почнете використовувати застосунк “PhotoShare”, вам потрібно встановити його. Дотримуйтесь цих кроків:

1. Клонуйте репозиторій на свій комп'ютер :white_check_mark::    

```
git clone https://github.com/Dmytro-Ostrenko/API_Wizards
```

2. Перейдіть в каталог проєкту :white_check_mark::    

```
cd API_Wizards
```

3. Встановіть “PhotoShare”  як Python-пакет :white_check_mark::
```
pip install . 
```

4. Далі встановлюємо poetry (віртуальне оточення) :white_check_mark::
```
pip install poetry 
```

5. Оновлюємо залежності встановленних бібліотек :white_check_mark::
```
poetry update
```

6. Та активуємо віртуальне середовище :white_check_mark::
```
poetry shell
```


##  <p align="center">Налаштування та з'єднання із БД</p>     
Для початку роботи із БД переконайтесь, що у Вас встановлено та оновлені до останньої версії наступні програми:

* DockerDesktop (посилання для завантаження з [офіційного сайту](https://www.docker.com/products/docker-desktop/).)
* DBeaver (посилання для завантаження:   з [офіційного сайту](https://dbeaver.io/download/).  )

Після відкриття програм  DBeaver та DockerDesktop, спершу налаштуємо з'єднання та запустимо контейнер у DockerDesktop, для цього вже було створено файл docker-compose.yml :white_check_mark: для цього виконуємо команду:
```
docker compose up -d
```
Вірно налаштування з'єднання у DBeaver потребує вказати значення: 
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


##  <p align="center">Робота із застосунком “PhotoShare” </p>   

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

### Запит на підтвердження пошти

- **Опис**: Відправлення запиту на підтвердження пошти для підтвердження облікового запису користувача.
- **Шлях**: `/auth/request_email`
- **Метод**: `POST`
- **Вхідні Параметри**:
    - `email`: Пошта користувача, для якого потрібно відправити запит на підтвердження пошти (обов’язкове поле).
- **Результат**: Відправляє листа на вказану поштову скриньку користувача з посиланням для підтвердження пошти. Якщо адреса вже підтверджена, повертає повідомлення "Вашу пошту вже підтверджено".

### Підтвердження пошти за допомогою токену

- **Опис**: Підтвердження пошти користувача за допомогою токену, отриманого на пошту.
- **Шлях**: `/auth/confirmed_email/{token}`
- **Метод**: `GET`
- **Вхідні Параметри**:
    - `token`: Унікальний токен, який був надісланий на поштову скриньку користувача (обов’язкове поле).
- **Результат**: Підтверджує адресу електронної пошти користувача. Якщо адреса вже підтверджена, повертає повідомлення "Ваша електронна адреса вже підтверджена".


### Примітка:
Аутентифікація та авторизація: Відбувається реєстрація нового користувача. Далі відбуваэться підтвердження пошти. Перший користувач у системі - "адміністратор", решта за замовчанням має роль "користувача". Роль може змінити "адміністратор".

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


##  <p align="center">Структура проекту застосунку "PhotoShare" </p> 
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
- `.env`: текстовий файл, який містить змінні середовища для конфігурації для додатку;
- `migrations`: зберігаються файли міграцій для бази даних.

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

:ghost:    Примітка:Слідкуйте за інструкціями програми та вводьте дані у відповідному форматі.
------



#  <p align="center">:robot:  API_Wizards:robot:  </p>     
# <p align="center"> *:smiley_cat: Reading language - English. Instructions for installing and using the “PhotoShare” application (REST API)*</p>
## Introduction

Welcome to API_Wizards! This is a REST API application called "PhotoShare". 

## Prerequisites

Make sure you have Python version 3.11 or newer installed on your computer. You can download Python from the [official website](https://www.python.org/downloads/).

## Installation

Before you start using the "PhotoShare" application, you need to install it. Follow these steps:

1. Clone the repository to your computer:

```
git clone https://github.com/Dmytro-Ostrenko/API_Wizards
```

2. Navigate to the project directory :white_check_mark::    

```
cd API_Wizards
```

3. Install "PhotoShare" as a Python package :white_check_mark::
```
pip install . 
```

4. Next, install poetry (virtual environment) :white_check_mark::
```
pip install poetry 
```

5. Update the dependencies of installed libraries :white_check_mark::
```
poetry update
```

6. Then activate the virtual environment :white_check_mark::
```
poetry shell
```

Now you're all set to use the "PhotoShare" application! Enjoy sharing photos with ease.

## Setting up and connecting to the database

Before working with the database, make sure you have the following programs installed and updated to the latest version:

* DockerDesktop (download link from the [official website](https://www.docker.com/products/docker-desktop/))
* DBeaver (download link from the [official website](https://dbeaver.io/download/))

After opening DBeaver and DockerDesktop, first, configure the connection and start the container in DockerDesktop. For this purpose, a `docker-compose.yml` file has already been created. Execute the following command to start the container:
```
docker compose up -d
```
Proper configuration of the connection in DBeaver requires specifying the following values: 
- name DB
- user
- password
- ports
 
Since the project already contains a pre-created database (located in migrations/versions), we skip the step of creating it. This is handled by the command :white_check_mark::
```
alembic revision --autogenerate -m 'Init'
```

After configuring the connection correctly, execute the following command to update the database :white_check_mark::
```
alembic upgrade head
```

Finally, to start FastAPI, execute the following command :white_check_mark::
```
uvicorn main:app --reload   
``` 
Once done, the application "PhotoShare" will be accessible at: http://127.0.0.1:8000. Additionally, you can access the Swagger documentation at: http://127.0.0.1:8000/docs.

## Working with the "PhotoShare" application

### Authorization in the application:

#### Registration

- **Description**: Register a new user.
- **Path**: `/auth/signup`
- **Method**: `POST`
- **Input Parameters**:
  - `username`: Username of the new user (required field).
  - `email`: Email of the new user (required field).
  - `password`: Password (required field).
- **Result**: Creates a new user in the database.

#### Login

- **Description**: Authorization of an existing user.
- **Path**: `/auth/login`
- **Method**: `POST`
- **Input Parameters**:
  - `email`: Email of the existing user (required field).
  - `password`: Password (required field).
- **Result**: Authorizes the user in the system, determines their role, and provides corresponding functionality in the application.

#### Changing user roles (functionality available only to administrators)

- **Description**: Authorization of an existing user.
- **Path**: `/auth/change_role`
- **Method**: `POST`
- **Input Parameters**:
  - `admin_email`: Administrator's email (required field).
  - `user_email`: Email of the user whose role will be changed (required field).
  - `new_role`: New role in the database (required field).
- **Result**: Changes the user's role.

### Request Email Confirmation

- **Description**: Sends a request for email confirmation to verify the user's account.
- **Path**: `/auth/request_email`
- **Method**: `POST`
- **Input Parameters**:
    - `email`: The user's email to send the email confirmation request to (required).
- **Result**: Sends an email to the specified user's email address with a link for email confirmation. If the address is already confirmed, returns the message "Your email is already confirmed".

### Email Confirmation via Token

- **Description**: Confirms the user's email address using the token sent to their email.
- **Path**: `/auth/confirmed_email/{token}`
- **Method**: `GET`
- **Input Parameters**:
    - `token`: The unique token sent to the user's email address (required).
- **Result**: Confirms the user's email address. If the address is already confirmed, returns the message "Your email address is already confirmed".

### Note:
Authentication and authorization: Registration of a new account is required. You will then be prompted to confirm your postage. The first manager in the system is the “administrator”, and the role of the “corruption manager” is responsible for the duties. The role can be changed to "administrator".

### Managing Photos in the Application:

#### Uploading a Photo

- **Description**: Upload a new image.
- **Path**: `/photos/`
- **Method**: `POST`
- **Input Parameters**:
    - `file`: Image file to upload (required field).
- **Result**: The image is successfully uploaded to the system.

#### Updating Photo Description

- **Description**: Update the description of an existing image.
- **Path**: `/photos/{photo_id}`
- **Method**: `PUT`
- **Input Parameters**:
    - `body`: Request body with the new photo description.
    - `photo_id`: ID of the image to update (required field).
    - `description`: New description for the image (required field).
- **Result**: The image description is successfully updated.

#### Deleting a Photo

- **Description**: Delete an existing image.
- **Path**: `/photos/{photo_id}`
- **Method**: `DELETE`
- **Input Parameters**:
    - `photo_id`: ID of the image to delete (required field).
- **Result**: The image is successfully deleted from the system.

#### Getting Information about a Photo

- **Description**: Retrieve information about an existing image.
- **Path**: `/photos/`
- **Method**: `GET`
- **Input Parameters**:
    - `url`: URL of the image to retrieve information for (required field).
- **Result**: Information about the image.

#### Resizing a Photo

- **Description**: Resize an existing image.
- **Path**: `/photos/resize`
- **Method**: `POST`
- **Input Parameters**:
    - `url`: URL of the image to resize (required field).
    - `width`: New width of the image.
    - `height`: New height of the image.
- **Result**: The image is resized according to the specified parameters.

#### Cropping a Photo

- **Description**: Crop an existing image.
- **Path**: `/photos/crop`
- **Method**: `POST`
- **Input Parameters**:
    - `url`: URL of the image to crop (required field).
    - `width`: Width of the new image.
    - `height`: Height of the new image.
- **Result**: The image is cropped according to the specified parameters.

#### Applying Filter and Text to a Photo

- **Description**: Apply a filter and text to an existing image.
- **Path**: `/photos/apply-filter-text`
- **Method**: `POST`
- **Input Parameters**:
    - `url`: URL of the image to apply the filter and text to (required field).
    - `filter_name`: Name of the filter to apply.
    - `text`: Text to add to the image.
    - `font_family`: Font family of the text.
    - `font_size`: Font size of the text.
    - `font_color`: Font color of the text.
- **Result**: The filter and text are successfully applied to the image.

#### Converting Photo Format

- **Description**: Convert an existing image to another format.
- **Path**: `/photos/convert-format`
- **Method**: `POST`
- **Input Parameters**:
    - `url`: URL of the image to convert (required field).
    - `new_format`: New format of the image.
- **Result**: The image is converted to the new format.

#### Getting Photo Metadata

- **Description**: Retrieve metadata about an existing image.
- **Path**: `/photos/get-metadata`
- **Method**: `POST`
- **Input Parameters**:
    - `url`: URL of the image to retrieve metadata for (required field).
- **Result**: Metadata about the image.

#### Getting a Link to the Transformed Photo

- **Description**: Retrieve a link to an existing transformed image.
- **Path**: `/photos/{transformed_photo_id}`
- **Method**: `GET`
- **Input Parameters**:
    - `transformed_photo_id`: ID of the transformed image.
- **Result**: A link to the transformed image.

#### Getting a QR Code for a Photo

- **Description**: Generate a QR code for an existing image.
- **Path**: `/photos/get_qr_code/{transformed_photo_id}/`
- **Method**: `GET`
- **Input Parameters**:
    - `transformed_photo_id`: ID of the transformed image.
- **Result**: QR code for the image.

### Managing Comments on Photos:

#### Creating a Comment

- **Description**: Create a new comment on a photo.
- **Path**: `/comments/`
- **Method**: `POST`
- **Input Parameters**:
    - `comment`: Comment object containing the comment text, photo ID, and user ID (required field).
    - `photo_id`: ID of the photo to which the comment is added (required field).
    - `user_id`: ID of the user adding the comment (required field).
- **Result**: The comment is successfully created.

#### Getting Comments on a Photo

- **Description**: Get comments on a specific photo.
- **Path**: `/comments/{photo_id}/comments`
- **Method**: `GET`
- **Input Parameters**:
    - `photo_id`: ID of the photo for which comments are retrieved (required field).
- **Result**: Comments on the photo.

#### Updating a Comment

- **Description**: Update an existing comment.
- **Path**: `/comments/{comment_id}`
- **Method**: `PUT`
- **Input Parameters**:
    - `comment_id`: ID of the comment to update (required field).
    - `comment`: Comment object with the new comment text (required field).
- **Result**: The comment is successfully updated.

#### Deleting a Comment

- **Description**: Delete an existing comment.
- **Path**: `/comments/{comment_id}`
- **Method**: `DELETE`
- **Input Parameters**:
    - `comment_id`: ID of the comment to delete (required field).
- **Result**: The comment is successfully deleted.

## Project Structure of the "PhotoShare" Application

- `main.py`: the main program file containing FastAPI routes.
  - `src/`: directory containing the application logic.
  - `src/conf/`: directory containing the application configurations.
  - `src/database/`: directory with database configurations and models.
  - `src/repository/`: directory with repository classes for interacting with the database.
  - `src/routes/`: directory containing FastAPI router modules.
  - `src/schemas/`: schemas used for data validation and interaction within the software.
  - `src/services/`: files related to business logic and software functionality.
- `pyproject.toml`: Poetry configuration file containing project dependencies.
- `docker-compose.yml`: Docker Compose configuration file used to define and configure multi-container applications. The file contains descriptions of services composing the application as well as Docker container environment setup parameters.
- `.env`: text file containing environment variables for application configuration.
- `migrations`: directory storing migration files for the database.

## P.S. Additional Information

### Filter Names for Image Processing in Cloudinary and Their Functions:

- grayscale: Converts the image to grayscale.
- sepia: Adds a vintage effect to the image.
- blackwhite: Converts the image to high-contrast black and white.
- saturation: Controls the color saturation in the image.
- brightness: Adjusts the brightness of the image.
- contrast: Controls the contrast between colors in the image.
- blur: Blurs the image, creating a blur effect.
- sharpen: Increases the sharpness of the image.
- hue: Changes the color tone in the image.
- invert: Inverts the colors in the image.

:ghost: Note: Follow the program instructions and enter data in the appropriate format.
------











