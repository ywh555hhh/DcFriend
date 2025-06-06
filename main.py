import discord
from discord.ext import commands
import asyncio
import config
from utils.database_handler import init_db

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents) # 前缀无所谓，我们用提及

@bot.event
async def on_ready():
    print("----------------------------------------")
    print(f'看板娘已登录：{bot.user}')
    print(f"在 Discord 服务器中 @{bot.user.name} 即可与我互动。")
    print("----------------------------------------")

async def main():
    # 在启动前，初始化数据库
    # 这确保了如果数据库文件不存在，它会被创建
    init_db()

    print("正在加载功能模块...")
    await bot.load_extension("cogs.conversation_cog")
    print(" - cogs.conversation_cog 已加载")

    print("看板娘正在启动...")
    await bot.start(config.DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("看板娘正在关闭。")
    except Exception as e:
        print(f"启动时发生致命错误：{e}")