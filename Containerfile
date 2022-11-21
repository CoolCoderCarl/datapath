FROM python:3.9-alpine as builder

COPY ["datapath.py", "/opt/"]
COPY ["dynaconfig.py", "/opt/"]
COPY requirements.txt requirements.txt

RUN pip3 install -U pip
RUN pip3 install --no-cache-dir -r requirements.txt

FROM builder

CMD ["python3.9", "/opt/datapath.py"]