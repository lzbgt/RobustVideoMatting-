from celery import Celery


class CeleryConfig:
    task_serializer = "pickle"
    result_serializer = "pickle"
    event_serializer = "json"
    accept_content = ["application/json", "application/x-python-serialize"]
    result_accept_content = ["application/json",
                             "application/x-python-serialize"]


celery = Celery('tasks', backend='rpc://',
                broker='pyamqp://guest:Huayuan@2020@localhost//')

celery.config_from_object(CeleryConfig())

# class SingletonClass(object):
#   def __new__(cls):
#     if not hasattr(cls, 'instance'):
#       cls.instance = super(SingletonClass, cls).__new__(cls)
#     return cls.instance

# class SingletonChild(SingletonClass):
#     pass
