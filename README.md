# boogie

Discord bot to communicate with OpenAI api

This was a quick-hit, fun project to learn about Discord bots and an excuse
to set up a Docker container. The bot itself is a simple relay between Discord
events and the OpenAI API.

## Setup

Setting everything up requires configuring a couple of different places - the
Discord Developer Portal, your Discord Server, and deploying to Docker.

### Create a Discord bot

- Go to the [Discord Developer Portal](https://discord.com/developers/applications)
- Create a new application (I called mine Boogie)
- Go to the Bot tab and click "Add Bot"
- Copy the Bot Token to some place safe
- Give it a username and profile picture
- Enable the Intents you want to use (I enabled all of them)
- Go to OAuth2 and select the "bot" scope
- Enable the following bot permissions:
  - View Channels
  - Send Messages
  - Read Message History
- Copy the URL and paste it into your browser
- Select the server you want to add the bot to
- Go to the Bot tab and copy the token

### Authorize bot in Discord server

- Go to your Discord server settings
- Edit categories and/or channels for where you want the bot to appear
- Add the same bot permissions as above

### Running the bot locally with uv

- Clone this repository
- If needed, install uv via 'brew install uv'

```sh
uv sync
source .venv/bin/activate
uv run bot.py
```

### Deploy the bot to Docker (Optional)

- Clone this repository
- Edit the Dockerfile with your `DISCORD_TOKEN` (Bot Token) and `OPENAI_API_KEY`
- Build the Docker image: `docker build -t boogie .`
- Run the Docker container: `docker run -d boogie --name boogie-box`

At this point you should see the bot appear in your Discord server.

## Usage

You can interact with the bot by sending messages in the channels you've given
it access to.

`/ask` will send a message to the OpenAI API and return the response.

`/clear` will clear the chat history between the user and OpenAI.

Note:

- Conversations are maintained per user, so you can have multiple conversations
  going at once.
- Conversations span channels so you can start a conversation in one channel
  and continue it in another.
- Conversations are cleared when the bot is restarted.
- Conversations are not stored in the bot (although the text is stored on
  Discord).
