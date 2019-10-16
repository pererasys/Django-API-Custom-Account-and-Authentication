**Basic Information**

This is a custom authentication system to be used by REST API's created with Django-rest-framework.

To allow for phone verification, make an account with Twilio and include your account information in\
the project settings file, (src/src/settings.py).


**Setup**
1. Clone this repository
2. Run pipenv shell
3. Run pipenv install (to install all required dependencies)
4. Once inside the virtual environment, cd into the main src directory
5. Run "python3 manage.py makemigrations", followed by "python3 manage.py migrate".
6. You are now ready to start the server, run "python3 manage.py runserver"
