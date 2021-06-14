FROM python:3.7.5-slim-buster

EXPOSE 8000

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY project /project
WORKDIR /project

# CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]
# More suitable for production would be using asgi+uvicorn instead of "runserver"
CMD ["gunicorn", "project.asgi:application", "-b", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker"]
