# DiscordValley
DiscordValley, the farming simulator for Discord! Brought to you by the DV team.


# Using docker compose
On the first run postgres won't have a database. You have to manually create it.    
```
docker-compose up db
docker exec -it discordvalley_db_1 psql -U postgres
create database bot;
exit
```
Now kill the container with CTRL+C and run all together
```
docker-compose up
```