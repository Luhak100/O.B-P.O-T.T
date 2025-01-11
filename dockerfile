FROM python:>=3.11
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]

RUN apt-get update && apt-get install -y cmake
RUN apt-get update && apt-get install -y libcairo2-dev
