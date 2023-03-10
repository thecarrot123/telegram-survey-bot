FROM python:3.8 as base

# Data installing
WORKDIR /app
COPY . .

# Install requrements
RUN python -m pip install --upgrade pip
RUN pip install -r requirement.txt

ARG SQLALCHEMY_TEST_DATABASE_URI
ARG SQLALCHEMY_DATABASE_URI
ARG SECRET_KEY
ARG BOT_TOKEN

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SQL_HOST db
ENV SQL_PORT 5432
ENV SQLALCHEMY_TEST_DATABASE_URI=$SQLALCHEMY_TEST_DATABASE_URI
ENV SQLALCHEMY_DATABASE_URI=$SQLALCHEMY_DATABASE_URI
ENV SECRET_KEY=$SECRET_KEY
ENV BOT_TOKEN=$BOT_TOKEN
ENV FLASK_APP=main.py

# Test 
FROM base as test
ENV APP_SETTINGS="flask_config.TestConfig"
RUN mkdir -p instance
RUN mv test.sqlite3 instance
CMD ["python3", "bot.py"]


# Product
FROM base as product
RUN [ -f .env.dev ] && export $(cat .env.dev | xargs)
ENV APP_SETTINGS="flask_config.ProductionConfig"
CMD ["python3", "bot.py"]