FROM python:3.11
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY atproto-nodeinfo-gen ./atproto-nodeinfo-gen/
RUN find /app
ENTRYPOINT ["python3", "-m", "atproto-nodeinfo-gen"]
