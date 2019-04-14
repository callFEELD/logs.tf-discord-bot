FROM python:3.6
WORKDIR /logdiscordbot
COPY LogDiscordBot/ ./
RUN pip install asyncio
RUN pip install discord.py==0.16.6

CMD ["python", "./run.py"]
