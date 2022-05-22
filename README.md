# Fleo Assignment

### Steps to Setup Backend

Make sure you have python 3.10 and pipenv installed on your pc.

Then follow these steps:
```
cd <project-directory>/
cp .env.example .env
```  
```
pipenv --python 3.10 install --dev
```

- Activate the new virtual environment:
```
pipenv shell
cd <project-directory>/backend/
```  
- Make database migrations (Make sure to setup postgres database with user and password and update the same in the .env file)
```
python manage.py makemigrations
python manage.py migrate
```  
- Create a superuser
```
python manage.py createsuperuser
```  
- Run development server on localhost
```
python manage.py runserver
```  

- Use tools like Postman/Insomnia/Curl to test the backend API endpoints