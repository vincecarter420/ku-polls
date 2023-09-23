1. clone the repositori into your computer
```
https://github.com/vincecarter420/ku-polls.git
```

2. change your directory to the project
```
cd ku-polls
```

3. create virtual environment and activate it

On Mac/Linux:
```
python -m venv myenv
source myenv/bin/activate
```
On Window:
```
python -m venv myenv
myenv\Scripts\activate
```

4. create `.env` file

On Mac/Linux
```
cp simple.env .env 
```
On Windows
```
copy simple.env .env
```

5. install Python dependencies by using `pip`
```
pip install -r requirements.txt
```

6. apply migrations
```
python manage.py makemigrations
python manage.py migrate
```

7. load data from users and polls.json
```
python manage.py loaddata data/polls.json 
python manage.py loaddata data/users.json
```

8. run development server
```
python manage.py runserver
```
