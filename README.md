# planner-fastapi

RUN

    $ pip3 install -r requirements.txt
    $ pip3 main.py

TEST

    $ pytest
    $ coverage run -m pytest
    $ coverage report
    $ coverage html

.ENV

    DATABASE_URL=mongodb+srv://...
    SECRET_KEY=*****

.ENV.PROD

    DATABASE_URL=mongodb://database:27017/planner
    SECRET_KEY=***

Docker

    $ docker compose up -d
    $ docker compose down
