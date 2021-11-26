celery -A app.tasks.video_proc worker --loglevel=INFO
 uvicorn app:app --host=0.0.0.0 --port=5000