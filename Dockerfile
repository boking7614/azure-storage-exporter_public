FROM ubuntu:20.04
LABEL type="azure-storage-exporter"

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3.9-dev python3-pip && apt-get clean
COPY app/ /app
RUN pip install --no-cache-dir -r /app/requirements.txt


EXPOSE 8092

WORKDIR /app

CMD ["python3","exporter.py"]