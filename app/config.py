from celery import Celery
from decouple import config


class CeleryConfig:
    task_serializer = "pickle"
    result_serializer = "pickle"
    event_serializer = "json"
    accept_content = ["application/json", "application/x-python-serialize"]
    result_accept_content = ["application/json",
                             "application/x-python-serialize"]


MQTT_URL = config('mqtt')

celery = Celery('tasks', backend='rpc://',
                broker=f'pyamqp://{MQTT_URL}//')

celery.config_from_object(CeleryConfig())

# class SingletonClass(object):
#   def __new__(cls):
#     if not hasattr(cls, 'instance'):
#       cls.instance = super(SingletonClass, cls).__new__(cls)
#     return cls.instance

# class SingletonChild(SingletonClass):
#     pass
