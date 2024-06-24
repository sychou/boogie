# Use an official Python runtime as a parent image
FROM python:3.11-alpine

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV DISCORD_TOKEN=
ENV OPENAI_API_KEY=

# Run bot.py when the container launches
CMD ["python", "bot.py"]
