# !!!Before you deploy this code!!!
- This program is **only intended to use** within the localhost/docker-incapsulated network. By exposing it to LAN or WAN you severely risk your fb account's safety
- The microservice itself doesn't provide any kind of security against DDOS attack so you have to configure the clients to restrict any kind of unauthorized access. The fastapi framework works asynchronously and the parser has been written in a proper way to not block any kind of IO, so it is possible that attacker may try to send infinite requests in purpouse of killing the server by opening infinite amount of webdriver instances

## Deploy Strategy:
Rename ```example.json``` to ```config.json```, open it and enter your data