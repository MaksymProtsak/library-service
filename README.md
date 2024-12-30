# Library service Project
<hr>

DRF project for library service

## Installation

Python 3 must be already installed

```commandline
git clone https://github.com/MaksymProtsak/library-service.git
cd library-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver  # starts Django Server
```

## Run with docker
<hr>

```commandline
docker-compose build
docker-compose up
```

## Getting access
<hl>

* created user via /api/user/register/
* get access token via /api/user/token/
* refresh access token via /api/user/token/refresh/

## Features

* Authentication functionality for Customer/Admin
* Managing books and borrowings directly from website interface
* Powerful admin panel form advanced managing
* Documentation is located at api/doc/swagger/

## Crated admin (superuser) in docker container
1. Check running containers 
`docker-composer ps`
    ```
    NAME                                IMAGE                             COMMAND                  SERVICE           CREATED          STATUS          PORTS                 
    library-service-db-1                postgres:16.0-alpine3.17          "docker-entrypoint.s…"   db                36 seconds ago   Up 34 seconds   0.0.0.0:5432->5432/tcp
    library-service-library_service-1   library-service-library_service   "sh -c 'python manag…"   library_service   36 seconds ago   Up 34 seconds   0.0.0.0:8001->8000/tcp
    ```
2. Enter inside `library_service` container (the name from SERVICE column) with `sh` command.

    `library-service>docker-compose exec library_service sh`

3. Create superuser with `createsuperuser` command `python manage.py createsuperuser`.
4. Enter email and password of new superuser.

## Demo
Login user succeed 
![Login user succeed](demo_images/login_user_successed.png)

User info page
![User info page](demo_images/api_user_me.png)

Token refresh page
![Token refresh page](demo_images/token_refresh_page.png)

Books app routes
![Book app routes](demo_images/books_app_routes.png)

Books list
![Books list](demo_images/books_list.png)

Book retrieve
![Book_retrieve](demo_images/book_retrieve.png)

Borrowing app routes
![Borrowing routes](demo_images/borrowings_app_routes.png)

Borrowing list
![Borrowing list](demo_images/borrowings_list.png)

Borrowing retrieve
![Borrowing_retrieve](demo_images/borrowings_retrieve.png)

Borrowing return
![Borrowing_return](demo_images/borrowings_return.png)

