# TDARR Stats

### A web interface that shows you quick stats when you upload your Tdarr CSV.

You can access the interface on port 5000 of your local machine, and then upload your Tdarr CSV.
All the processing is done on the machine that is running the python script/container so you should be able to upload from your phone & any other low power devices. 

![Desktop Screenshot](/examples/Desktop_Screenshot.png)

Docker compose file:

```
services:
  tdarr-stats:
    container_name: tdarr-stats
    image: alyssaholland99/tdarr-stats
    restart: unless-stopped
```
^^ docker-compose.yml

Bring up the container
```
docker compose up -d
```
