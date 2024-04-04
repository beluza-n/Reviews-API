# Reviews API
Authors:
* gatart (Teamlead, Auth/Users)
* beluza-n (Categories/Genres/Titles)
* Vladimir-V-K (Review/Comments)

## Desicription
Group project during training at Yandex Prakticum. Uses Django Rest Framework.
The project collects user reviews of various works of art. User can register, create review for a book / film / movie, comment reviews of other users.

## Stack:
* Python
* Django Rest Framework
* JWT

### How to run the project:
Clone repository and go to it with the terminal::

```
git clone https://github.com/beluza-n/Reviews-API.git
```

```
cd Reviews-API
```

Create and activate virtual environment:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Update pip (optional):

```
python -m pip install --upgrade pip
```

Install dependencies from the requirements.txt:

```
pip install -r requirements.txt
```

Run migrations:

```
python manage.py migrate
```

Launch the Django project:

```
python manage.py runserver
```

## API request examples

### Get confirmation code / Register
You must send a POST request to the path `/api/v1/auth/signup/`.
A confirmation code will be sent by email.
Request to the server:
```json
{
"email": "user@example.com",
"username": "string"
}
```

Server response:
```json
{
"email": "string",
"username": "string"
}
```
### Get a token
You need to send a GET request to the path `/api/v1/auth/token/`.
Request to the server:
```json
{
"username": "string",
"confirmation_code": "string"
}
```
Server response:
```json
{
"token": "string"
}
```
### Other requests
You can find other requests in the API documentation:
`/redoc/`
