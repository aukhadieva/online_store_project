# online_store_project

<!-- ABOUT THE PROJECT -->
## О проекте
*Django-проект интернет-магазина*

- В проекте представлено приложение с названием *catalog*.
- Внесены начальные настройки Django-проекта.
- Проведена настройка урлов (URL-файлов).
- Реализованы два контроллера: 
    - Контроллер, который отвечает за отображение домашней страницы.
    - Контроллер, который отвечает за отображение контактной информации.
- Реализована обработка сбора обратной связи от пользователя, который зашел на страницу обратной связи и отправил свои данные.

<!-- GETTING STARTED -->
## Подготовка к работе

Чтобы запустить локальную копию, выполните следующие простые шаги:

### Установка

1. Клонируйте проект
   ```sh
   git@github.com:aukhadieva/online_store_project.git
   ```
2. Убедитесь, что вы получили из удаленного репозитория все ветки и переключились на ветку разработки develop
   ```sh
   git checkout develop
   ```
3. Установите зависимости проекта (в случае, если не установились при клонировании)
   ```sh
   poetry install
   ```

### Запуск приложения
1. Для того, чтобы запустить проект, выполните команду
   ```sh
   python3 manage.py runserver
   ```
2. Пройдите по адресу
   ```sh
   http://127.0.0.1:8000/
   ```
