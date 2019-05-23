FROM python:3.5
COPY . /app
WORKDIR /app
RUN pip install -r requirement.txt
EXPOSE 5000
RUN ["pip", "install", "flask"]
CMD ["flask", "run", "-h", "0.0.0.0"]

