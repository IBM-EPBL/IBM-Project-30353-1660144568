FROM python:3.9
LABEL maintainer="Samyuktha, 713319cs124@smartinternz.com"
RUN apt-get update
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install flask
RUN pip install flask_session
RUN pip install ibm-db
RUN pip install ibm_db
RUN pip install sendgrid
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
