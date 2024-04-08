FROM python:3.12.1-alpine

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/* /root/.cache

CMD ["hypercorn", "-b", "0.0.0.0:3000", "--keep-alive", "10", "app:app"]

