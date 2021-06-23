# the-list-bot

The bot that powers https://list.futbol

You can run it yourself by filling in your credentials in the config.yaml file and running main.py

## Docker

The bot is also a runnable Docker image on [DockerHub](https://hub.docker.com/repository/docker/midasvo/the-list)

Create a volume that overrides the config.yaml file in order to customize the configuration


## Major todos:

- Add logging, should be able to cat a file and see what the bot has done

- Add database logging instead of in a text file

- Add better recognition of callouts

- Ability to watch comments to see if they meet the threshold of being added

- Ability to respond to help requests by giving a short explanation on how the bot and site works

- Ability to update a reply once the PR is merged