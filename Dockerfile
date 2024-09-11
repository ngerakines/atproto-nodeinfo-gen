FROM python:3.11-alpine
LABEL org.opencontainers.image.source=https://github.com/ngerakines/atproto-nodeinfo-gen
LABEL org.opencontainers.image.description="Generate well-known nodeinfo files for an ATProtocol PDS."
LABEL org.opencontainers.image.licenses=MIT
WORKDIR /app
RUN --mount=type=bind,source=requirements.txt,target=requirements.txt pip install --no-cache-dir -r requirements.txt
COPY atproto-nodeinfo-gen ./atproto-nodeinfo-gen/
ENTRYPOINT ["python3", "-m", "atproto-nodeinfo-gen"]
