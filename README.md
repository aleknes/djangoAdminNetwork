# What This Is
A starter template for using Django Admin Site as an CMDB and automation tool for network equipment. The template includes the app `networkProvisioning`
with a sample `models.py` and `admin.py` for demonstrating on how models can be built to achieve this. It inludes a demo action inside `admin.py`
which demonstrate how to iterate through equipment and perform an action on each.

It also includes a custom javascript with necessary operations for demonstrating how buttons can be added anywhere to the UI to trigger and handle python scripts in the backend.

This starter only support backend operations which take a few seconds to execute. this is to avoid browser timeout. To handle operations that takes several minutes or more, a backend worker like celery must be used.
This is not included in this demo.

## Installation

### Prerequisites

Make sure you are running Python Version 3.10 or newer and Git CLI installed.

If you're unfamiliar with what Django is and how it works it's wise to go through a tutorial first: https://www.w3schools.com/django/

### Download repository

```
git clone https://github.com/bentole/djangoAdminNetwork.git
cd djangoAdminNetwork
```

### Create virtual environment
```
python3 -m venv venv
source venv/bin/activate # At least on Linux/Mac OS
pip install -r requirements.txt
```

## Run Project

`python manage.py runserver`

## Accessing the Admin Site

http://127.0.0.1:8000/admin and log in with bol/bol

You'll see three models/db tables available under NetworkProvisioning: `Routers`, `Serial Numbers`, `Sites` and `Switches`. 

Whats important to note is that normally you'd only have to enter `Site` to view `Routers` and `Switches` as well. These models are so called inlines to the Site model. Inside these inlines is where you probably would want to to have actions available to users in form of buttons, dropdowns and such. A sample action button for this can be found inside Sites -> testsite1 -> Routers
