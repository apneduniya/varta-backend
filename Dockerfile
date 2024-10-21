FROM python:3.11


WORKDIR /code


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt  


COPY . /code


CMD ["fastapi", "run", "main.py", "--port", "80"]