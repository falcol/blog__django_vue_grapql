**Installation**
For the backend, first create a virtual environment.

```
cd backend
python3 -m venv env
source env/bin/activate
```

Install required packages.

`pip install -r requirements.txt`

Run migrations.

```
python manage.py makemigrations
python manage.py migrate
```

# FRONT END ERROR, CANNOT USE
# CANNOT USE APPOLO UPLOAD FILE WITH VUE VITE

Start dev server.

`python manage.py runserver`
For the frontend, install packages.

```
cd frontend
npm install
```

If you are getting errors when installing packages, just run npm install --force. Some packages has been deprecated, but everything still work for now. I will try to update this project as soon as possible.

Start frontend dev server.

`npm run dev`
