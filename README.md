# !!!Before you deploy this code!!!
- This program is **only intended to use** within the localhost/docker-incapsulated network. By exposing it to LAN or WAN you severely risk your fb account's safety
- The microservice itself doesn't provide any kind of security against DDOS attack so you have to configure the clients to restrict any kind of unauthorized access. The fastapi framework works asynchronously and the parser has been written in a proper way to not block any kind of IO, so it is possible that attacker may try to send infinite requests in purpouse of killing the server by opening infinite amount of webdriver instances

## API endpoints:
To see all of API's endpoints, go to ```localhost:8000/docs```
Powered by OpenAPI

## Deploy Strategy:
Rename ```example.json``` to ```config.json```, open it and enter your data

# TODO List:
- [x] Add Config parsers
- [x] Add robust Exception handling
- [x] Add logging
- [ ] Add Docker Support
- [ ] Write tests
  - [x] Tests for config.py
  - [ ] Tests for gecko-webdriver
  - [x] Tests for utils.py
- [ ] Documentation
  - [x] API endpoints
  - [ ] Configuration guide
  - [ ] Deployment instructions
- [ ] Security Improvement
  - [ ] Login by creds
  - [ ] Limit the maximum amount of concurrent connections