# 1Shot Discord Bot Demo

This is a minimal example of how to leveral 1Shot API in a Discord Bot. 

## 1. Create a Discord App

Visit the [Discord application console](https://discord.com/developers/applications) and create a new bot. You'll need to generate a bot token and keep it somewhere safe. 

## 2. Build the bot Docker image

Clone this repo and build the bot container image:

```sh
docker build -t bot . 
```

## 3. Run the bot container

With your token from step 1, run the bot container:

```sh
docker run -d --rm --name bot -e DISCORD_BOT_TOKEN=<your-token> bot
```

## 4. Add the bot to your server

Add the bot to you server and invoke one of its commands. 