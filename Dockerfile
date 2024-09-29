FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["CMD must be overridden during container instantiation. Use 'tail -f /dev/null' to do nothing but keep the container running."]
