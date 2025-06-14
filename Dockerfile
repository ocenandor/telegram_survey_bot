FROM python:3.12-slim

# WORKDIR /app

# Install git and clean up cache
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Clone the repo (you can change the repo URL)
# RUN git clone https://github.com/ocenandor/telegram_survey_bot.git /app
# Install Python dependencies
COPY ./requirements.txt  /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /app
CMD ["python", "main.py"]
# CMD ["bash"]