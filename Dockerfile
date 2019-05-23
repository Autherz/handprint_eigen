FROM python:3.5
COPY . /app
WORKDIR /app
RUN pip install -r requirement.txt
ENTRYPOINT   ["python"]
CMD ["app.py"]

