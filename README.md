# Random number generator API 
  - Rate limiting service on top on each authenticated user (5 requests allowed per minute)

### Endpoints
* [127.0.0.1] - Start Page
* [127.0.0.1/signup] - Sign up page with username and password
* [127.0.0.1/login] - Login page for authentication
* [127.0.0.1/call_api] - Calls the random number api and outputs the number received (only can be accessed if user is authenticated and has not exhausted the limit else returns 403 error)
* [127.0.0.1/see_remaining_limits] - Returns the remaining requests for the user in that minute (only can be accessed if user is authenticated else returns 403 error)
* [127.0.0.1/logout] - logs out the user

### Docker Commands to make app run

To be executed in Random-Generator folder

```sh
$ docker build -t randomapi .
$ docker-compose up
```
# Description

* Created API A (Random number generator Service) using Fastapi
* Remaining endpoints were built using Flask
* For Rate-limiting, in-memory database (Redis) is Used 
* Authentication using SQLAlchemy, flask-login 
