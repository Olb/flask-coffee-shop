# Full Stack Coffee Shop API

## Introduction

This project is a coffee shop app that allows users to view drinks, baristas can view drinks and see ingredients and managers can create, edit, and update drinks. The objective is to demonstrate API Authentication and Authorization. Specifically, this API requires JWT tokens from Auth0.

Backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

### Installing Backend Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

It is generally recommended, but not required, to use a virtual environment.

[python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM used to handle the lightweight sqlite database.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to handle cross origin requests from the frontend server.

### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=api.py
export FLASK_ENV=development
flask run
```

### Testing

To run the tests, create a sqlite database called `test_drinks.py` in the /src directory and add a single drink. Change `self.manager_token` and `self.barista_token` in test_drinks.py to valid tokens. Then, from the /src directory run

```
python test_drinks.py
```

### Installing Frontend Dependencies

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing Ionic Cli

The Ionic Command Line Interface is required to serve and build the frontend. Instructions for installing the CLI is in the [Ionic Framework Docs](https://ionicframework.com/docs/installation/cli).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

## Required Tasks

### Configure Enviornment Variables

Ionic uses a configuration file to manage environment variables. These variables ship with the transpiled software and should not include secrets.

- Open `./src/environments/environments.ts` and ensure each variable reflects the system you stood up for the backend.

## Running Your Frontend in Dev Mode

Ionic ships with a useful development server which detects changes and transpiles as you work. The application is then accessible through the browser on a localhost port. To run the development server, cd into the `frontend` directory and run:

```bash
ionic serve
```

> [Checkout the Ionic docs to learn more](https://ionicframework.com/docs/cli/commands/build)

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.

- Authentication: This version of the application does not require API keys but does require an Auth0 JWT token for all create, update, and delete requests. A token is also required for drink details.

### Error Handling

Error are returned as JSON objects in the following format

```
{
'message':'Bad request',
'error': 400,
'success':False
}
```

The API will return four error types when requests fail:

- 400
- 401
- 403
- 404
- 422
- 500

### Endpoint Library

#### Get /drinks

- General:

  - Returns a list of drink objects and success value.

- Sample: `curl http://127.0.0.1:5000/drinks`

```
{
  "drinks": [
    {
      "id": 1,
      "recipe": [
        {
          "color": "green",
          "parts": 1
        }
      ],
      "title": "Super Green"
    }
  ],
  "success": true
}
```

#### GET /drinks-detail

- General:

  - Returns a list of drinks and success value. The drinks contain recipe information.
  - Requires barista or manager permissions role.

- Sample: `curl http://127.0.0.1:5000/drinks-detail`

```
{
  "drinks": [
    {
      "id": 1,
      "recipe": [
        {
          "color": "green",
          "name": "Green Beast",
          "parts": 1
        }
      ],
      "title": "Super Green"
    }
  ],
  "success": true
}
```

#### DELETE /drinks/{drink_id}

- General:
  - Deletes a drink with the provided ID. Returns the success value and the deleted drink's ID.
  - Requires manager permissions role.
- Sample: `curl -X DELETE \ http://localhost:5000/drinks/2 \ -H 'Accept: */*' \ -H 'Accept-Encoding: gzip, deflate' \ -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJFSTJNVFF3UXpoR1JEQTRRMFJETVVGRE5VTkJRVVUwUmtVNU9FUXhNMEUzTmtOQ016RkRSQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYmlsbHkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVkODYyYzMwNGVmMDMyMGRmNGU0YWU5NiIsImF1ZCI6ImRyaW5rcyIsImlhdCI6MTU2OTI3NjY2OSwiZXhwIjoxNTY5MzYzMDY5LCJhenAiOiJybFVOaURqalMwQlA2bzBYSHJiNGYyU0ZobEUwRnJEMCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkcmlua3MiXX0.cqm-TZaSALiLlm9zeSOHCiasJltDet4-76yDUOIrkM4bH0VZG2-whg5b0fxV-dxyOjKwHtd2fBt-V-hFgzonO6CfpL2G0CsWmfrSTmex5sMJL24YA5ZotX1HsLENntsjza2OCMvBxMiE0HFD8qdekMndweWYxeE5YON-L_0SIYg0RVpZ1WInaEuArh40n-bD84E3fDleczuxslGUSc873rQ6k_2kfI-IxUj-57iezSDmoGEXgUdexi_1sO2eyZ6F3En4Jj0Aka5p5rfps09Bro9uGYIitCFsTh_k7nuHi-KQE80ReZjIONtUNT-G-68tQ2yMyNqtM5Dmorvtb1f5Yw' \ -H 'Cache-Control: no-cache' \ -H 'Connection: keep-alive' \ -H 'Content-Length: 0' \ -H 'Host: localhost:5000' \ -H 'Postman-Token: 672de643-2ebe-410a-9777-4b84ee0bdd4d,3ec05d51-16f6-4f5a-8cfa-0c767c9da4b3' \ -H 'User-Agent: PostmanRuntime/7.17.1' \ -H 'cache-control: no-cache'`

```
{
  "delete": 2,
  "success": true
}
```

#### POST /drinks

- General:

  - Creates a new drink using the title and recipe. Returns the success value and the created drink JSON.
  - Requires manager permissions role

- Sample: `curl -X POST \ http://localhost:5000/drinks \ -H 'Accept: */*' \ -H 'Accept-Encoding: gzip, deflate' \ -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJFSTJNVFF3UXpoR1JEQTRRMFJETVVGRE5VTkJRVVUwUmtVNU9FUXhNMEUzTmtOQ016RkRSQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYmlsbHkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVkODYyYzMwNGVmMDMyMGRmNGU0YWU5NiIsImF1ZCI6ImRyaW5rcyIsImlhdCI6MTU2OTI3NjY2OSwiZXhwIjoxNTY5MzYzMDY5LCJhenAiOiJybFVOaURqalMwQlA2bzBYSHJiNGYyU0ZobEUwRnJEMCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkcmlua3MiXX0.cqm-TZaSALiLlm9zeSOHCiasJltDet4-76yDUOIrkM4bH0VZG2-whg5b0fxV-dxyOjKwHtd2fBt-V-hFgzonO6CfpL2G0CsWmfrSTmex5sMJL24YA5ZotX1HsLENntsjza2OCMvBxMiE0HFD8qdekMndweWYxeE5YON-L_0SIYg0RVpZ1WInaEuArh40n-bD84E3fDleczuxslGUSc873rQ6k_2kfI-IxUj-57iezSDmoGEXgUdexi_1sO2eyZ6F3En4Jj0Aka5p5rfps09Bro9uGYIitCFsTh_k7nuHi-KQE80ReZjIONtUNT-G-68tQ2yMyNqtM5Dmorvtb1f5Yw' \ -H 'Cache-Control: no-cache' \ -H 'Connection: keep-alive' \ -H 'Content-Length: 101' \ -H 'Content-Type: application/json' \ -H 'Host: localhost:5000' \ -H 'Postman-Token: 883faf85-ac59-47cb-905d-f87711a3845e,c2effc73-bfa7-45ba-aa38-3e8ff7d06eb6' \ -H 'User-Agent: PostmanRuntime/7.17.1' \ -H 'cache-control: no-cache' \ -d '{ "title": "Watera2", "recipe": [{ "color":"green", "name":"Green Beast", "parts": 1 }] }'`

```
{
  "drinks": [
    {
      "id": 2,
      "recipe": [
        {
          "color": "green",
          "name": "Green Beast",
          "parts": 1
        }
      ],
      "title": "Green Machine"
    }
  ],
  "success": true
}
```

#### PATCH /drinks/{drink_id}

- General:

  - Updates the drink with the provided ID. Returns the success value and the JSON for the updated drink.
  - Requires manager permissions role

- Sample: `curl -X PATCH \ http://localhost:5000/drinks/1 \ -H 'Accept: */*' \ -H 'Accept-Encoding: gzip, deflate' \ -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJFSTJNVFF3UXpoR1JEQTRRMFJETVVGRE5VTkJRVVUwUmtVNU9FUXhNMEUzTmtOQ016RkRSQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYmlsbHkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVkODYyYzMwNGVmMDMyMGRmNGU0YWU5NiIsImF1ZCI6ImRyaW5rcyIsImlhdCI6MTU2OTI3NjY2OSwiZXhwIjoxNTY5MzYzMDY5LCJhenAiOiJybFVOaURqalMwQlA2bzBYSHJiNGYyU0ZobEUwRnJEMCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkcmlua3MiXX0.cqm-TZaSALiLlm9zeSOHCiasJltDet4-76yDUOIrkM4bH0VZG2-whg5b0fxV-dxyOjKwHtd2fBt-V-hFgzonO6CfpL2G0CsWmfrSTmex5sMJL24YA5ZotX1HsLENntsjza2OCMvBxMiE0HFD8qdekMndweWYxeE5YON-L_0SIYg0RVpZ1WInaEuArh40n-bD84E3fDleczuxslGUSc873rQ6k_2kfI-IxUj-57iezSDmoGEXgUdexi_1sO2eyZ6F3En4Jj0Aka5p5rfps09Bro9uGYIitCFsTh_k7nuHi-KQE80ReZjIONtUNT-G-68tQ2yMyNqtM5Dmorvtb1f5Yw' \ -H 'Cache-Control: no-cache' \ -H 'Connection: keep-alive' \ -H 'Content-Length: 101' \ -H 'Content-Type: application/json' \ -H 'Host: localhost:5000' \ -H 'Postman-Token: 138ab962-cac0-4745-a14a-76f4af900798,3055a0b8-65df-41e1-8377-b77d7d667367' \ -H 'User-Agent: PostmanRuntime/7.17.1' \ -H 'cache-control: no-cache' \ -d '{ "title":"Super Green", "recipe": [{ "color":"green", "name":"Green Beast", "parts": 1 }] }'`

```
{
  "drinks": [
    {
      "id": 1,
      "recipe": [
        {
          "color": "green",
          "name": "Green Beast",
          "parts": 1
        }
      ],
      "title": "Super Green"
    }
  ],
  "success": true
}
```
