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
git clone https://github.com/<username>/<repository>
```

Navigate into project root and run 
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

Open browser and navigate to 
```
http://localhost:8000/
```