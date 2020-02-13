FROM python:3
RUN mkdir /isb
WORKDIR /isb
COPY requirements.txt /isb/requirements.txt
RUN pip install -r requirements.txt
COPY . /isb/
CMD python manage.py runserver 0.0.0.0:8000
