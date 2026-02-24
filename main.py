import random
import discord
from discord.ext import commands
from datetime import datetime, timezone, timedelta

bot = commands.Bot(
    command_prefix=">",
    intents=discord.Intents.default()
)

QUOTES = [
    "Keep going.",
    "You are doing better than you think.",
    "Small steps still move you forward.",
    "Progress over perfection.",
    "Consistency beats motivation.",
    "Be loyal to your own peace of mind.",
    "You're your only limit.",
    "Prove yourself to yourself not to others.",
    "Nobody is too busy, it's just a matter of priorities.",
    "Life is like rhyme, one line at a time.",
    "In the face of pain there are no heroes. You're the hero.",
    "Silence isn't empty. It's just full of answers.",
    "Change the world by being yourself.",
    "Your best teacher is your last mistake.",
    "Do not live bowing down. You must die standing up"
]

# user_id -> date (UTC)
daily_usage = {}

@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="/quote"
        )
    )
    print(f"Orin is ready as {bot.user}")

@bot.tree.command(
    name="quote",
    description="Get your daily motivational quote"
)
async def quote(interaction: discord.Interaction):
    user_id = interaction.user.id
    now_utc = datetime.now(timezone.utc)
    today = now_utc.date()

    if daily_usage.get(user_id) == today:
        next_reset = datetime.combine(
            today + timedelta(days=1),
            datetime.min.time(),
            tzinfo=timezone.utc
        )
        remaining = next_reset - now_utc
        hours = remaining.seconds // 3600
        minutes = (remaining.seconds % 3600) // 60

        await interaction.response.send_message(
            f"🌙 Daily limit reached.\n"
            f"Next quote in **{hours}h {minutes}m** (00:00 UTC).",
            ephemeral=True
        )
        return

    daily_usage[user_id] = today
    await interaction.response.send_message(
        random.choice(QUOTES),
        ephemeral=True
    )


bot.run(os.getenv("DISCORD_TOKEN"))
