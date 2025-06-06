# main.py
import discord
import config  # 确保这个导入在最前面，以便尽早检查配置
import asyncio

# 定义 Bot 的 Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# 我们将使用 Client，因为它更轻量，适合我们只用事件的场景
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    """当 Bot 成功登录并准备好时调用。"""
    print("----------------------------------------")
    print(f'Bot 已登录，用户名为：{bot.user}')
    print(f'Bot 的用户 ID 为：{bot.user.id}')
    print(f"在 Discord 服务器中 @{bot.user.name} 即可与我互动。")
    print("----------------------------------------")

@bot.event
async def on_message(message: discord.Message):
    """当收到消息时调用。"""
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        print(f"在频道 #{message.channel} 中被 {message.author} 提及。")
        
        # 阶段二的测试回复
        await message.reply("连接测试成功！我已经能听到你的呼唤了。")

async def main():
    """异步主函数，用于启动 Bot。"""
    # 在这里，我们将不再调用 init_db()，因为主程序只负责启动 Bot
    # 数据库的初始化和管理可以由单独的脚本或首次运行时处理
    # 这样保持了主程序的单一职责
    try:
        print("正在启动 dcfriend Bot...")
        await bot.start(config.DISCORD_BOT_TOKEN)
    except discord.errors.LoginFailure:
        print("错误：Discord Bot Token 无效。请检查服务器上的.env 文件。", file=sys.stderr)
    except Exception as e:
        print(f"启动 Bot 时发生致命错误：{e}", file=sys.stderr)

if __name__ == "__main__":
    # 这是一个好的实践：确保我们的 utils 也能独立工作
    # 如果直接运行 main.py，就启动 bot
    asyncio.run(main())