FROM lzbgt/nvpytorch:11.3

WORKDIR /build

COPY build /build
COPY build/.env build/.env
RUN printf '#!/bin/bash\n\
nohup celery -A app.tasks.video_proc worker -c2 --loglevel=INFO &disown &\n\
uvicorn app:app --host=0.0.0.0 --port=5000'\
>entrypoint.sh && \
chmod +x entrypoint.sh
# ENTRYPOINT ["conda", "run", "-n", "cuda", "uvicorn", ""]
EXPOSE 5000
CMD ["./entrypoint.sh"]