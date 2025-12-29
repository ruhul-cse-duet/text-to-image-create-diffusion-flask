FROM pytorch/pytorch:2.2.0-runtime

WORKDIR /app

# system deps (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# copy files
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

ENV FLASK_APP=run.py
ENV PYTHONUNBUFFERED=1
EXPOSE 5000

# small startup script chosen to allow easy override
CMD ["bash", "start.sh"]
