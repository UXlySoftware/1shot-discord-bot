
[![Watch the tutorial](https://img.youtube.com/vi/LIz4ANRdPus/maxresdefault.jpg)](https://youtu.be/LIz4ANRdPus)

# 1Shot Discord Bot Demo

This is a minimal example of how to leverage 1Shot API in a Discord Bot. 

## 1. Create a Discord App

Visit the [Discord application console](https://discord.com/developers/applications) and create a new bot. You'll need to generate a bot token and keep it somewhere safe. 

## 2. Create a 1Shot API Account

Log into 1Shot and create a new API key and secret from the [API Keys](https://app.1shotapi.com/api-keys) page. You'll need both the client ID and
secret for your bot. 

Also, go to the [Organizations page](https://app.1shotapi.com/organizations) and click on the "Details" button of your org. Grab the business ID from the url. 

## 3. Create a 1Shot API Endpoint

Make sure you have [created and funded](https://app.1shotapi.com/escrow-wallets) an Escrow Wallet on the Sepolia Network. On the [Endpoints](https://app.1shotapi.com/endpoints) page, import [0xA1BfEd6c6F1C3A516590edDAc7A8e359C2189A61](https://sepolia.etherscan.io/address/0xA1BfEd6c6F1C3A516590edDAc7A8e359C2189A61) on the Sepolia testnet. 

Click on the details of the function `deployToken` and the the endpoint Id. 

## 4. Build the bot Docker image

Clone this repo and build the bot container image:

```sh
docker build -t bot . 
```

## 5. Run the bot container

Gather your Discord bot token, API key and secret, business id, and endpoint id to run the bot container:

```sh
docker run -d --rm --name bot -e DISCORD_BOT_TOKEN=<get-a-token-from-discord> -e API_KEY=<1Shot-API-Key> -e API_SECRET=<1Shot-API-Secret> -e BUSINESS_ID=<Your-1Shot-Busines-ID> -e ENDPOINT_ID=<deployToken-endpoint-id> bot
```

## 6. Add the bot to your server

Add the bot to you server and invoke `/deploy_token`. 

![Demo of the bot in action](deploy-token.gif)
