FROM python:3.6
WORKDIR /logdiscordbot
COPY LogDiscordBot/ ./
RUN pip install asyncio
RUN pip install discord.py

CMD ["python", "./run.py"]
