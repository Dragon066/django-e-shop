# E-shop in Django

This project contains frontend & backend for online store, running on [Django Framework v5.0.7](https://github.com/django/django) in Python.

![image](https://github.com/user-attachments/assets/553a2c38-2f04-4895-a6d8-dced890a117a)

## 💥 Features:

- Registration and authorization using JWT
- Product catalog, the ability to add and manage your own products
- Shopping cart
- Order system, the ability to check orders for your products from other users
- API with [Django REST Framework](https://github.com/encode/django-rest-framework)

## 🔨 Installation

> #### 1. Clone this repository

Clone this repository to your local machine:

    git clone https://github.com/Dragon066/django-e-shop

Move to the repository directory:

    cd .\django-e-shop\

> #### 2. Create virtual environment and install required dependencies

Create virtual environment (*Note: here and further, if you are on a Linux, use `python3` instead of `python`*):

    python -m venv venv

Activate just created environment (*Note for Linux: `source .\venv\Scripts\activate`*):

    .\venv\Scripts\activate

Install all required dependencies that are written in `requirements.txt`:

    pip install -r requirements.txt

> #### 3. Make migrations

Go to the main directory of the project `eshop`: 

    cd .\eshop\

Make migrations and migrate models to create sqlite3 database:

    python manage.py makemigrations

>

    python manage.py migrate

To change database management system you can use [official notes](https://docs.djangoproject.com/en/5.0/ref/databases/) about databases in Django.

> #### 4. Create superuser

To make your first admin account, use the command below:

    python manage.py createsuperuser

Type E-mail (any, even non-existent), first and last name (also), password. Bypass password validation if you wish.

> #### (Additional) 5. Fill the database with test data from fixture

To get acquainted with the functionality you can use fixture to load some products into your database:

    python manage.py loaddata products.json

Make sure that you have created at least one user (check stage 4).

> #### 6. Run server

Finally, run your server!

    python manage.py runserver

You can access E-shop website at default address http://127.0.0.1:8000/.

## 🎯 URLs

There is a list of available urls in this project:

- [`/catalog/`](http://127.0.0.1:8000/catalog/) - main page (also redirects here from `/`) with list of all products
- `/accounts/`
  - [`/accounts/registration/`](http://127.0.0.1:8000/accounts/registration/) - registration page
  - [`/accounts/login/`](http://127.0.0.1:8000/accounts/login/) - login page
  - [`/accounts/profile/`](http://127.0.0.1:8000/accounts/profile/) - profile page
- [`/cart/`](http://127.0.0.1:8000/cart/) - shopping cart
- `/order/`
  - [`/order/my_orders/`](http://127.0.0.1:8000/order/my_orders/) - list of user's orders
  - [`/order/client_orders/`](http://127.0.0.1:8000/order/client_orders/) - list of orders for user products
- `/api/v1/` - API reference
- [`/swagger/`](http://127.0.0.1:8000/swagger/) - documentation for API with Swagger (in [drf-yasg](https://github.com/axnsan12/drf-yasg/tree/master))
- [`/admin`](http://127.0.0.1:8000/admin/) - Django admin panel
