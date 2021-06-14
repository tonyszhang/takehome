# Hello World, Autodesk!
This is Tony's submission for the Autodesk DPI(ADP?) take-home challenge.
The application is created using the Python Django web framework and features:
* Docker container artifact that can be deployed to any environment/OS
* Instructions for local development and deployment using Pipenv
* Pinned dependencies for reproducibility
* Logging configurations for either Docker/Pipenv
* Simple PoC CI/CD pipeline leveraging CircleCI and Google Kubernetes Engine

## OS-independent Build, Deployment, and Test
For deployment, the application is containerized to be as portable as possible.
This only assumes Docker Engine 18.09 or later [to be installed](https://docs.docker.com/get-docker/).
1. `docker build .` which returns an IMAGE_ID
    - Uses the production-grade command `gunicorn project.asgi:application -k uvicorn.workers.UvicornWorker` (later: can try this locally after `cd project` and `pipenv shell`)
2. `docker run -it -p 8000:8000 <IMAGE_ID>` 
3. Test app in different terminal with `curl http://127.0.0.1:8000/ -H "Accept: application/json"` (header optional)
4. For unit tests, run `docker run -it <IMAGE_ID> python manage.py test` 

## Local Development/Testing installation instructions
For local development and improving the app, pipenv is used.
The only assumption is [Python 3.7 (with pip) installed](https://www.python.org/downloads/release/python-3710/) on either a Linux, MacOS, or WSL workstation.
1. `pip install pipenv` (can also do this outside of pip e.g. MacOS `brew install pipenv`) 
    and `export PIPENV_VENV_IN_PROJECT="enabled"`
2. In repo root, `pipenv install --dev --python 3.7.5` and `pipenv shell`
3. `cd project` and `python manage.py runserver` to start the local dev server
4. Test app (separate terminal window) with `curl http://127.0.0.1:8000/` or `curl http://127.0.0.1:8000/ -H "Accept: application/json"` to see locahost server response.
5. Run unit tests with `python manage.py test`
6. Materialize pip requirements `pipenv lock -r > requirements.txt` to be used with Dockerfile

## Logging
Django uses Python’s builtin logging module to perform system logging.
By default, Django uses the dictConfig format, configured inside of settings.LOGGING dictionary.
Logging level is by default INFO which does not include the request URL log. To turn on request URL logs:
- If running in Docker mode, use `docker run --env API_LOGLEVEL=DEBUG -it -p 8000:8000 <IMAGE_ID>`
- If running in pipenv mode, use `API_LOGLEVEL=DEBUG python manage.py runserver`
- If running on kubernetes, add `API_LOGLEVEL=DEBUG` to deployment `spec.template.spec.containers.[0].env`

## Cloud and CI/CD
- Included is a simple `k8s/manifest.yaml` file for use with `kubectl` once the CI/CD service account is granted access to a hosted k8s cluster (via GCP service accounts).
- The `.circleci/config.yml` defines a basic pipeline which tests branch commits before merging into main and pushes a new docker image to Container Registry.
- A human operator can approve the "Hold" step which then deploys the image tagged with "latest"


## Other information
- The project was bootstrapped using `django-admin startproject project` and `cd project && python manage.py startapp hello` with a `pipenv shell` session. There are hence auto-generated boilerplate files inside of `project/` dir.
- `pipenv` is a personal convenience choice, but could have been replaced by Python3's built-in `venv`