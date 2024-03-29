FROM ubuntu:latest

# Set environment variable for Discord bot token
#ENV DISCORD_TOKEN=<your-discord-bot-token>

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip  && \
#    apt install -y open-jtalk open-jtalk-mecab-naist-jdic ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Copy the Discord bot files to the container
RUN mkdir -p /app
COPY . /app

# Install Python dependencies
RUN pip3 install -r /app/requirements.txt

# Set the working directory
WORKDIR /app

# Set the DISCORD_TOKEN environment variable before running the bot
#CMD ["bash", "-c", "export DISCORD_TOKEN=$DISCORD_TOKEN && python3 main.py"]
CMD ["python3", "main.py"]
