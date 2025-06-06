import discord
from discord.ext import commands
import google.generativeai as genai
import json
import config
from utils import database_handler

class ConversationCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.model = None
        self.persona = {}
        self._load_persona()
        self._configure_ai()

    def _load_persona(self):
        with open(config.PERSONA_FILE_PATH, 'r', encoding='utf-8') as f:
            self.persona = json.load(f)
        print(f"人格 '{self.persona.get('name')}' 加载成功。")

    def _configure_ai(self):
        genai.configure(api_key=config.GOOGLE_AI_KEY)
        self.model = genai.GenerativeModel('models/gemini-2.5-flash-preview-05-20')
        print(f"Google AI 模型配置成功，使用模型：{self.model.model_name}")

    def _format_history_for_prompt(self, history: list[dict]) -> str:
        if not history:
            return "（没有历史对话）"
        formatted_lines = [f"{row['user_name']}: {row['content']}" for row in history]
        return "\n".join(formatted_lines)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user or not self.bot.user.mentioned_in(message):
            return

        user_prompt = message.content.replace(f'<@{self.bot.user.id}>', '', 1).replace(f'<@!{self.bot.user.id}>', '', 1).strip()
        if not user_prompt:
            await message.reply(f"你好，我是{self.persona.get('name', '汐')}。有什么可以聊聊的吗？")
            return
        
        print(f"收到来自 {message.author.name} 的消息：{user_prompt}")

        async with message.channel.typing():
            try:
                # 1. 获取历史
                recent_history = database_handler.get_recent_dialogue(limit=10)
                formatted_history = self._format_history_for_prompt(recent_history)
                
                # 2. 构建 Prompt
                system_instruction = f"{self.persona['identity']}\n你的性格特点是：{', '.join(self.persona['personality_traits'])}"
                prompt = f"{system_instruction}\n\n--- 对话历史 ---\n{formatted_history}\n\n--- 新的问题 ---\n{message.author.name}: {user_prompt}\n{self.persona.get('name', 'AI')}:"

                # 3. 调用 AI
                response = await self.model.generate_content_async(prompt)
                ai_reply = response.text

                # 4. 发送回复 & 记录数据库
                await message.reply(ai_reply)
                database_handler.add_dialogue_event(message.author.id, message.author.name, 'user', user_prompt)
                database_handler.add_dialogue_event(self.bot.user.id, self.persona.get('name', 'AI'), 'model', ai_reply)
                print("对话已记录到数据库。")

            except Exception as e:
                print(f"处理消息时发生错误：{e}")
                await message.reply("抱歉，我的思绪有点混乱，稍后再试试吧。")

async def setup(bot: commands.Bot):
    await bot.add_cog(ConversationCog(bot))