# Main Project Idea

A simple survey in telegram without
seeking out external survey providers. Since many organizations use telegram as an information resource
to know about deadlines, new events, and many more things; I wanted to create something that is
contained within the telegram platform itself.

# What Is This Repo
This repo contains a demo of the main idea with simple backend while focusing more on the DevOps side of the project (for educational purposes).

## Repo Core Points:
* The server was created using ```python-telegram-bot==13.15``` to communicate with Telegram, ```Flask==2.2.3``` and ```Flask-SQLAlchemy==3.0.3``` and manage the admin page and the database.
* One Docker file was implemented to build two images: test image and product image. The test image uses an sqlite3 database (for simplicity) that has some basic data to test (test.sqlite3 file in the repo), while the product image will connect to a Postgres database.
* The production database is hosted on the server in separate docker container ```postgres:13-alpine``` that is managed by the docker-compose file.
* The docker-compose will manage and run both of the docker containers: the product (web) and the database (db).
* The workflow ```docker-image.yml``` handles building the docker images and running the tests before building and deploying the project to the server. The workflow runs on push and pull_request events on master branch.
* Sensitive data (secret keys, passwords, etc.) are saved as secrets in the repository and passed to the docker files. 


# How To Run

## Requirements

* ``` docker ```
* ``` docker-compose ```

## Test Image

 You need to set the `SQLALCHEMY_TEST_DATABASE_URI`, `SECRET_KEY`, and `BOT_TOKEN` environment variables.
Then run:
```bash
        docker build . \
        -t test_image \
        --target test \
        --build-arg SQLALCHEMY_TEST_DATABASE_URI \
        --build-arg SECRET_KEY \
        --build-arg BOT_TOKEN
``` 
> You can set `SQLALCHEMY_TEST_DATABASE_URI` as `sqlite:///test.sqlite3`

## Product Image

 You need to set the `SQLALCHEMY_DATABASE_URI`, `SECRET_KEY`, and `BOT_TOKEN` environment variables.
Then run:
```bash
        docker build . \
        -t telegram_survey_bot \
        --target product \
        --build-arg SQLALCHEMY_DATABASE_URI \
        --build-arg SECRET_KEY \
        --build-arg BOT_TOKEN
```
> `SQLALCHEMY_DATABASE_URI` has the following form: `postgresql://$POSTGRES_USER:$POSTGRES_PASS@db:5432/$POSTGRES_DB`

## Run Product
After building the product image you need to set the `POSTGRES_USER`, `POSTGRES_PASS`, and `POSTGRES_DB` environment variables.
Then run:
```bash
docker-compose build \
--build-arg POSTGRES_USER \
--build-arg POSTGRES_PASS \
--build-arg POSTGRES_DB
```
```bash
docker-compose up 
```
> Note that if you are running the product for the first you need to create the database by running this command in other terminal: 
```docker-compose exec web python manage.py create_db```
