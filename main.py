import nextcord
import datetime
import validators
from nextcord.ext import commands

TOKEN = ""
GUILD_ID = 1297978563370156134  

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"BOT NAME: {bot.user}")
    print(f"Connected to guilds: {[guild.name for guild in bot.guilds]}")
    await bot.change_presence(status=nextcord.Status.idle, activity=nextcord.Game("กำลังรอคำสั่ง..."))

class Announce(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(title="สร้างประกาศ")
        self.em_title = nextcord.ui.TextInput(
            label="ชื่อหัวข้อ",
            required=False
        )
        self.add_item(self.em_title)
        self.em_description = nextcord.ui.TextInput(
            label="รายละเอียดข้อความ",
            style=nextcord.TextInputStyle.paragraph,
            required=False
        )
        self.add_item(self.em_description)
        self.em_image = nextcord.ui.TextInput(
            label="ลิ้งรูปภาพ",
            required=False
        )
        self.add_item(self.em_image)
        self.em_color = nextcord.ui.TextInput(
            label="สีของ embed (hex code)",
            max_length=6,
            required=False
        )
        self.add_item(self.em_color)

    async def callback(self, interaction: nextcord.Interaction):
        color_value = int(self.em_color.value, 16) if self.em_color.value else 0xFFFFFF
        embed = nextcord.Embed(title=self.em_title.value, description=self.em_description.value, color=color_value)
        
        if validators.url(self.em_image.value):
            embed.set_image(url=self.em_image.value)
        
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text="ประกาศจากแอดมิน")
        
        await interaction.channel.send("@everyone", embed=embed)
        await interaction.send('สร้างประกาศสำเร็จ', ephemeral=True)

@bot.slash_command(guild_ids=[GUILD_ID], description='สร้างประกาศ | (admin only)')
async def announce(interaction: nextcord.Interaction):
    if interaction.user.guild_permissions.administrator:
        await interaction.response.send_modal(Announce())
    else:
        await interaction.send('มึงไม่มีสิทธิ์ใช้ครับไอ้โง่', ephemeral=True)

bot.run(TOKEN)
