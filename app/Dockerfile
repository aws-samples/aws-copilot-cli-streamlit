FROM python:3.9-slim
FROM huggingface/transformers-cpu:4.18.0
LABEL maintainer="Charles Frenzel"
LABEL org.webiste='https://aws.amazon.com/'

EXPOSE 8501

WORKDIR /app

COPY requirements.txt ./

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV LANG C.UTF-8

# hadolint ignore=DL3008
RUN apt-get update  \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# for to work locally in MAC must install and then uninstall
#RUN pip uninstall -y tensorflow-cpu

# hadolint ignore=DL3013
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . .

ENTRYPOINT ["streamlit", "run"]

CMD ["main.py"]
