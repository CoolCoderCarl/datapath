# FROM python:3.9-alpine as builder
FROM h0d0user/emperor_pandas:latest as builder

WORKDIR /opt/

COPY ["datapath.py", "/opt/"]
COPY ["dynaconfig.py", "/opt/"]

COPY requirements.txt requirements.txt

RUN pip3 install -U pip
RUN pip3 install --no-cache-dir -r requirements.txt
RUN apt update -y && \
    apt install curl jq -y

FROM builder

CMD ["python3.9", "datapath.py"]