# FastAPI application to store and retrieve events

## Requirements
- docker > 20
- python3
- Linux based-OS (tested on Fedora 40)

## Running the application
Make `run_now.sh` exectuable with 
```sh
# In the root folder
chmod +x run_now.sh
```

Use `run_now.sh` to:
- create a python3.12 virtual environment with all the required packages
- build a docker image
- run the docker image automatically

Once the image starts, use [http://localhost:8080/docs](http://localhost:8080/docs) to view the Swagger page.
All the steps in `run_now.sh` are quiet.

## Running the application in VSCode
To run the application separately in VS Code, you can:
- create a python virtual env with 
```sh
# In the root folder
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-all.txt
```
- in VS Code > Run and Debug > Dropdown > app > Start debugging (F5)

## Running the tests and pycoverage
If you do not have a virtual environment at this point, create one.
```sh
# In the root folder
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-all.txt
```

Then, run:
```sh
# In the root folder
pytest --cov-report term --cov=myapp myapp/tests/
```
