# Final Project

This is the readme for the final project.

Initial configuration:

1. setup django environment in vscode using command "python -m venv djangoenv"
2. activate virtual environment "djangoenv\Scripts\activate" [can deactive this by typing 'deactivate']
3. install django - "py -m pip install django"
4. gives version of installed django project - "django-admin --version"
5. create project "django-admin startproject product-sales"
6. start server with command "python manage.py runserver". http://127.0.0.1:8000/.
7. Create App 'python manage.py startapp sales'

Steps for Github workflow:

1. Pull main branch to get updated changes.
2. Merge main branch into your branch.
3. Check merge changes, make sure nothing is broken.
4. Merge your branch into main branch.

Loading JSON data from file to sqlite db:

1. create model in models.py and run commands
   python manage.py makemigrations
   python manage.py migrate
2. After the model is created, load data from input_data.json to the Item model. The corresponding code is in sales/management/commands/loadDB.py (python manage.py loadDB)

updating count on cards:

1. From home.html incCount(id) and decCount(id) to script.js. which inturn makes AJAX(Asynchronous JavaScript and XML) request to django backend without refreshing web page.
2. the request is handled in views.py to update the count and send a response.

cart page:

1. shows the image, name and quantity of product along with a delete button at end of each selected element.
2. delete button will remove element from cart and resets its count to zero.
3. the submit button at end will redirect to submit page.
