from celery import Celery

app = Celery('tasks',backend='rpc://', broker='pyamqp://guest:Huayuan@2020@localhost//')

@app.task
def add(x, y):
    return x + y