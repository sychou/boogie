import json
import os

import discord
import requests
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the tokens from environment variables
discord_token = os.getenv("DISCORD_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Dictionary to store conversation states for each user
conversation_history = {}

# OpenAI API endpoint
OPENAI_API_ENDPOINT = "https://api.openai.com/v1/chat/completions"


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


@bot.tree.command(name="ask", description="Ask OpenAI a question")
async def ask(interaction: discord.Interaction, message: str):
    print(f"User {interaction.user.id} asked: {message}")
    user_id = interaction.user.id
    if user_id not in conversation_history:
        conversation_history[user_id] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    # Defer the response immediately
    await interaction.response.defer()

    # Append the user's message to the conversation history
    conversation_history[user_id].append({"role": "user", "content": message})

    try:
        # Prepare the request payload
        payload = {"model": "gpt-4", "messages": conversation_history[user_id]}

        # Set up the headers
        headers = {
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json",
        }

        # Make the API call
        response = requests.post(OPENAI_API_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        # Parse the response
        response_data = response.json()
        assistant_reply = response_data["choices"][0]["message"]["content"]

        # Add the assistant's reply to the conversation history
        conversation_history[user_id].append(
            {"role": "assistant", "content": assistant_reply}
        )

        # Try to edit the original response
        try:
            await interaction.edit_original_response(content=assistant_reply)
        except discord.NotFound:
            # If editing fails, try to send a follow-up message
            await interaction.followup.send(content=assistant_reply)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        try:
            await interaction.edit_original_response(content=error_message)
        except discord.NotFound:
            await interaction.followup.send(content=error_message)


@bot.tree.command(name="new", description="Start a new conversation")
async def new(interaction: discord.Interaction):
    user_id = interaction.user.id
    # Clear the conversation history for the user
    conversation_history[user_id] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    await interaction.response.send_message(
        content="Conversation history cleared. You can start a new conversation."
    )


bot.run(discord_token)
