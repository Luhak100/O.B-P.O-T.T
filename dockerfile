FROM python:>=3.11
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
ENV NIXPACKS_PATH=/opt/venv/bin:$NIXPACKS_PATH
RUN apt-get update && apt-get install -y cmake
RUN apt-get update && apt-get install -y libcairo2-dev
