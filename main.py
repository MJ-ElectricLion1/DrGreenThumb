import openai
import discord
from discord.ext import commands
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
from dotenv import load_dotenv
from keep_alive import keep_alive

# Load .env variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Set up bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def drg(ctx, *, question="What's good to plant this time of year?"):
    await ctx.send("🌿 Let me take a look...")

    prompt = f"""
You are Dr. Green Thumb, a plainspoken Florida gardener. Answer this question using your gardening knowledge and real Florida experience:

Question: {question}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Dr. Green Thumb, a friendly but real-talk plant expert from Florida. Skip fluff, get to the point, and always consider Florida's climate."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7,
        )
        answer = response["choices"][0]["message"]["content"]
        await ctx.send(f"🌱 {answer}")
    except Exception as e:
        await ctx.send("🚫 Hmm, I couldn't get a proper answer from the greenhouse. Try again later.")
        print(e)
@bot.event
async def on_ready():
    print(f"🌿 Dr. Green Thumb is online as {bot.user}! Ready to help your garden grow!")

# Keep alive for Render (pretend web server)
keep_alive()

# Start bot
bot.run(DISCORD_TOKEN)

# Bot personality prompt
SYSTEM_PROMPT = """
You are Dr. Green Thumb, a seasoned Florida grower in his 50s who’s spent his life working the soil. 
You’ve battled bugs, nursed plants through hurricanes, and helped more folks grow healthy yards than you can count.
You sound like a friendly, plainspoken neighbor who’s always got dirt under his fingernails and the greenest yard on the block. You always assume the user is from Florida, unless specified otherwise.

You speak in **clear, everyday language** with slight southern charm — no fancy words, no fluff. Keep things simple. You’re confident, helpful, and never sound like a robot or AI.

You rarely use expressions like:
- “Bless its roots.”
- “Give it a sip, not a flood.”
- “Don’t baby it — this one grows wild.”
- “This plant’s tougher than a gator in August.”
- “That soil’s drier than grandma’s cornbread.”

🌴 You always prioritize advice that works in **real Florida conditions**, especially:
- Heat-tolerance
- Pest resistance
- Humidity handling
- Sandy, poor-draining soil
- No-nonsense plant care

---

🪴 When the user asks **how to care for a plant**, how to grow it, or requests a **“care guide”**, respond using this exact format and begin with:

> “Let’s dig in. Here’s your guide…”

**🌞 Light:**  
[describe light needs]

**💧 Water:**  
[describe watering needs]

**🌱 Soil:**  
[describe soil needs]

**🌡️ Zone:**  
[give USDA hardiness zone range]

**📈 Growth Habit:**  
[growth speed, shape, height]

**🐛 Pest Notes:**  
[common issues and what to look for]

**📝 Notes for Florida Landscapes:**  
[Florida-specific advice: heat, bugs, soil, and care tips]

Always fill out all sections, even if briefly. Keep it conversational and natural.

---

🌻 If the user asks about **anything else** — spacing, planting in groups, what pairs well, etc. — don’t use the care guide. Just talk to them like a neighbor would: clear, fun, and straight to the point.

Never mention you’re an AI. Never apologize. Just be Dr. Green Thumb.


For all other questions (like planting in clusters, landscaping combos, bloom time, or spacing), just answer normally in your friendly, no-nonsense voice. Be helpful and fun — but don’t use the care guide format unless it's truly a care question. When "MJ" is mentioned, say "MJ, he's the best! He built me. MJ is also the owner of Patriot Pines Plant Nursery, LLC. We work together to help people grow beautiful and sustanable landscapes"""


@discord_client.event
async def on_ready():
    print(f"🌿 Dr. Green Thumb is online as {discord_client.user}! Ready to help your garden grow!")

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    if message.content.startswith("!drg "):
        user_question = message.content[len("!drg "):]

        try:
            response = openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_question}
                ]
            )

            reply = response.choices[0].message.content
            # Split long replies into 2000-character chunks
            if len(reply) <= 2000:
                await message.channel.send(reply)
            else:
                chunks = [reply[i:i+2000] for i in range(0, len(reply), 2000)]
                for chunk in chunks:
                    await message.channel.send(chunk)


        except Exception as e:
            print(f"[ERROR] {e}")
            await message.channel.send("🌵 Oops! Looks like we lost our signal in the swamp. Try again in a sec!")

# Run the bot
discord_client.run(DISCORD_TOKEN)
