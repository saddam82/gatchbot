import discord
from discord.ext import commands
from discord.ui import View, Button
from PIL import Image, ImageDraw, ImageFont

# إعداد البوت
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# تخزين بيانات الشخصيات
characters = {
    "Diluc": {
        "element": "Pyro",
        "weapon": {"best": "Wolf's Gravestone", "free": "Prototype Archaic"},
        "artifact": "Crimson Witch of Flames",
        "stats": {"main": ["ATK%", "Pyro DMG Bonus", "CRIT DMG"], "sub": ["CRIT DMG", "CRIT Rate", "ATK%"]}
    },
    "Ganyu": {
        "element": "Cryo",
        "weapon": {"best": "Amos' Bow", "free": "Prototype Crescent"},
        "artifact": "Blizzard Strayer",
        "stats": {"main": ["ATK%", "Cryo DMG Bonus", "CRIT DMG"], "sub": ["CRIT Rate", "ATK%", "Energy Recharge"]}
    },
    # يمكنك إضافة المزيد من الشخصيات هنا
}

# إنشاء صورة للبناء
def generate_build_image(character_name, build):
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)

    # إعداد النصوص
    title_font = ImageFont.truetype("arial.ttf", 40)
    content_font = ImageFont.truetype("arial.ttf", 30)

    draw.text((50, 50), f"Character: {character_name}", fill="black", font=title_font)
    draw.text((50, 120), f"Element: {build['element']}", fill="black", font=content_font)
    draw.text((50, 180), f"Best Weapon: {build['weapon']['best']}", fill="black", font=content_font)
    draw.text((50, 240), f"Free Weapon: {build['weapon']['free']}", fill="black", font=content_font)
    draw.text((50, 300), f"Artifact Set: {build['artifact']}", fill="black", font=content_font)

    main_stats = ", ".join(build['stats']['main'])
    sub_stats = ", ".join(build['stats']['sub'])
    draw.text((50, 360), f"Main Stats: {main_stats}", fill="black", font=content_font)
    draw.text((50, 420), f"Sub Stats: {sub_stats}", fill="black", font=content_font)

    file_name = f"{character_name}_build.png"
    img.save(file_name)
    return file_name

# عرض واجهة الأزرار
class CharacterView(View):
    def __init__(self):
        super().__init__()
        for character in characters:
            self.add_item(Button(label=character, custom_id=character))

    @discord.ui.button(label="Diluc", style=discord.ButtonStyle.primary)
    async def show_diluc(self, button: Button, interaction: discord.Interaction):
        await self.show_character(interaction, "Diluc")

    async def show_character(self, interaction: discord.Interaction, character_name: str):
        if character_name not in characters:
            await interaction.response.send_message("Character not found. Please try again.")
            return

        build = characters[character_name]
        image_path = generate_build_image(character_name, build)

        with open(image_path, 'rb') as file:
            await interaction.response.send_message(file=discord.File(file))

@bot.event
async def on_ready():
    print(f"{bot.user} is now online!")

@bot.command()
async def start(ctx):
    view = CharacterView()
    await ctx.send("Select a character to view their build:", view=view)

# تشغيل البوت
bot.run("")
