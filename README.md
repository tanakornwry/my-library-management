# Library management system

## Database design structure
You can see my database design here https://dbdiagram.io/d/6296476e54ce26352734c52b

## How to install and set up the application
1. Prepare your Postgresql and create 2 new databases, one for Live database and one for test database.
2. Clone my git repository. Run this command.
    - `git clone git@github.com:tanakornwry/my-library-management.git`
3. Make sure your local device has the required libraries. Run this command at the project root directory.
    - `cd my-library-management`
    - `pip install -r requirements.txt`
4. Look at the project root directory, change the file name `.env.example` to `.env`
5. Modifies the value of `.env` on fields `SQLALCHEMY_DATABASE_URL` and `SQLALCHEMY_DATABASE_URL_TEST` to be your Postgresql's URL. Sample format has in the file.
    - `<username>`
    - `<password>`
    - `<databasename>`
6. Modifies `alembic.ini` on field `sqlalchemy.url` to your Postgresql's URL (same at the `SQLALCHEMY_DATABASE_URL`)
7. Create the database schemas by running this command 
    1. `alembic revision --autogenerate -m "Init"`
    2. `alembic upgrade head`
8. The application is ready to run...


## How to run the application
1. Run the application by this command at the project root directory
    - `uvicorn src.main:app`
2. FastAPI has the build-in OpenAPI, so it's easy to understand and use, what endpoints we have, what request data we should send for each endpoint, and what a scheme of each endpoint.
3. Access to this URL `http://127.0.0.1:8000/docs` 

If something goes wrong, please investigate what log console shows up and try to solve it :)


## How to run all test cases
1. Run all test cases by this command at the project root directory
    - `pytest tests`
2. Run this command at the project root directory to see all test cases coverage
    - `coverage run --source=src -m pytest -v tests && coverage report -m`
