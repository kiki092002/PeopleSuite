FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install flask
EXPOSE 8080
CMD ["python3","app.py"]