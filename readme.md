# Code Task


## Project initialization

Create a virtual environment in desired directory

```bash
python3 -m venv <name_of_virtualenv>
```

Activate the virtual environment 

```bash
source <name_of_virtualenv>/bin/activate
```

Clone repo into directory
```bash
git clone https://github.com/ikechukwueze/Code-Task.git
```

Navigate to project root and install dependencies
```bash
pip install -r requirements.txt
```

Create database tables 
```bash
python manage.py makemigration
python manage.py migrate
```

Seed database with initial data
```bash
python manage.py seed_rentals_data
```

Create superuser with username and password == "admin"
```bash
python manage.py create_admin_user
```

Start server
```bash
python manage.py runserver
```

Open a browser and navigate to 
```
http://localhost:8000/
```