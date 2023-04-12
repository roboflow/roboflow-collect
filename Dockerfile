FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY app.py .

# accept requirements
ENV ROBOFLOW_PROJECT=""
ENV ROBOFLOW_WORKSPACE=""
ENV ROBOFLOW_KEY=""
ENV SAMPLE_RATE=""
ENV COLLECT_ALL=""

# run the app
CMD ["python3", "app.py"]