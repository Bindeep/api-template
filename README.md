### Create django project with custom user and readymade authenticated url

##### Pull the code from the server.
```sh
django-admin startproject --template https://github.com/Bindeep/api-template/archive/master.zip <project_name>
```

##### Create virtual Environment
```sh
python3 -m venv .venv
```

##### Activate virtual Environment
```sh
source .venv/bin/activate 
```

##### Install requirements
```sh
pip install -r requirements/dev.txt
```

Copy env.sample.py file and create env.py with its content inside settings folder config folder

 
##### Migrate model to database
go inside project folder and make sure environment is activated
```sh
python manage.py migrate
```

##### Create superuser
```sh
python manage.py createsuperuser
```
fill all inputs to create superuser

##### Run Server
```sh
python manage.py runserver
```
