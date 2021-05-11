FROM python:3

RUN pip install flask
RUN pip install flask-sqlalchemy
RUN pip install flask-login


WORKDIR /app/

ENV FLASK_APP=__init__.py

COPY *.py /app/
COPY templates/ /app/templates/
COPY static/ /app/static/
COPY db.sqlite /app/

CMD ["/bin/sh", "-c", "python -m flask run --host=0.0.0.0 --port=$PORT"]