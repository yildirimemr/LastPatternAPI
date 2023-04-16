# LastPatternAPI
This repo contains a API application made using Python/Django/Django REST API(DRA) technologies.

## Getting Started
In the created application, Django REST API(DRA) is used for API endpoints and AppScheduler module is used for automaticly update database. Main features available in the application:
1. Obtaining stock market values of desired symbols via Binance APIs.
2. Generating technical indicator values over stock market values.
3. Pattern recognizing over stock market values.
4. Generating stock market predictions with obtained values.
5. Accessing generated predictions and statistics.

### Prerequisites
```
Python 10.0.x
aiohttp==3.8.3
aiosignal==1.3.1
APScheduler==3.10.1
asgiref==3.6.0
async-timeout==4.0.2
attrs==22.2.0
autopep8==2.0.1
certifi==2022.12.7
charset-normalizer==2.1.1
dateparser==1.1.5
Django==4.1.5
django-apscheduler==0.6.2
django-cors-headers==3.13.0
djangorestframework==3.14.0
frozenlist==1.3.3
idna==3.4
multidict==6.0.4
numpy==1.24.1
pandas==1.5.2
pandas-ta==0.3.14b0
pycodestyle==2.10.0
python-binance==1.0.16
python-dateutil==2.8.2
python-dotenv==1.0.0
pytz==2022.7
pytz-deprecation-shim==0.1.0.post0
regex==2022.10.31
requests==2.28.1
six==1.16.0
sqlparse==0.4.3
TA-Lib @ file:////packages/TA_Lib-0.4.24-cp310-cp310-win_amd64.whl
tomli==2.0.1
tzdata==2022.7
tzlocal==4.2
ujson==5.7.0
urllib3==1.26.13
websockets==10.4
yarl==1.8.2
```

### Installing and Usage
1. Project files are downloaded from this repository.
2. The virtual environment is set up and activated. It is recommended to have the virtual environment in the same folder as the project (in the same folder as manage.py). You can get help [here](https://medium.com/co-learning-lounge/create-virtual-environment-python-windows-2021-d947c3a3ca78) to set up the virtual environment.
3. After the virtual environment is activated, the `pip install requirements.txt` command must run.
4. You must create a .env file in the same folder manage.py. You can find and example .env file in the .env.example
5. The commands `python manage.py makemigrations` and `python manage.py migrate` are run respectively.
6. After the installation is finished, the `python manage.py createsuperuser` command is run and the Admin user is created.
7. With the `python manage.py runserver` command, the web application is run locally. The admin page can be reached at the address [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/). Then you need to login with your superuser name and password.
8. After login the admin panel you need to create a dummy record to StartPredictionScheduler table.
9. After that, select that record, start_workers from the combo box above, and press the go button.
10. Finally, you can observe the predictions from both in the admin panel and via api endpoints.

## Authors
* **Emre Yıldırım** - [GitHub](https://github.com/yildirimemr)