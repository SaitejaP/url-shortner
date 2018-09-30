# URL Shortener
A simple URL shortening service using Django

### API signature

**GET**  _/api/v1/urls/_

Get all url shortened


**POST**  _/api/v1/shorten/_

Shorten a long url

**Params**:

_long_url_: (URL|requried)


**GET** _/<short_url>/_

Redirects to long url if the path corresponds to any created short url 
