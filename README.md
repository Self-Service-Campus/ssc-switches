# switches

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9cb3dff776144b35956c91cc96b36c05)](https://app.codacy.com/gh/Self-Service-Campus/ssc-switches?utm_source=github.com&utm_medium=referral&utm_content=Self-Service-Campus/ssc-switches&utm_campaign=Badge_Grade_Settings)

## Add to final App
	* Files:
		- ConnectSW/__init_.pt
		- main/SwitchConnector.py
		- main/tasks.py
	* Celery Config -> add to settings.py:
		- INSTALLED_APPS = ['django_celery_results']
		- BROKER_URL = 'amqp://guest:**@localhost:5672//'
		- CELERY_RESULT_BACKEND = 'django-db'
		- CELERY_CACHE_BACKEND = 'django-cache'
	* Commands:
		$ pip3 install django-celery-results
		$ python manage.py migrate django_celery_results


## Install in VM
	* Rabbitmq
	* Celery
		- Run celery
			$ celery -A ConnectSW worker -l info
		NOTE: In Production is different
