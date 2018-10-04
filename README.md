# URL Shortener
A simple URL shortening service using Django

### Requirements ###
--------------------
python v3.7.0
pipenv v2018.7.1
postgres v10.5

### Setup ###
-------------
- Clone the repository
git clone https://github.com/SaitejaP/url-shortner.git

- Move into the directory
cd url-shortner/

- Install dependencies using pipenv
pipenv install

- Login to virtual environment
pipenv shell

- Move into the Django project
cd url_shortner/

- Create the environment file inside url_shortner app
vim url_shortner/.env

- `cat url_shortner/.env` file should give something like this
```
SECRET_KEY=vaKB6dg7x8h4gZY5b9YgSp82YpVTQznsHuJxmYy7jRCVs3YMYV
DEBUG=True
DATABASE_URL=postgres://postgres:ZKB2KrzhL@localhost:5432/url_shortner
```

- Now use ./manage.py to start the server
./manage.py runserver


### API signature ###
---------------------
**GET**  _/api/v1/urls/_

Get all url shortened


**POST**  _/api/v1/shorten/_

Shorten a long url

**Params**:

_long_url_: (URL|requried)


**GET** _/<short_url>/_

Redirects to long url if the path corresponds to any created short url 


### TO-DO ###
----------
[x] Creating a shortened url
[x] Fetching list of shortened urls
[x] Fetching original url from a shortened url
[ ] Deleting shortened-urls
[ ] Unit test cases
[ ] Use Redis to cache recently used short urls
[ ] Dockerize application
[ ] Deploy to AWS