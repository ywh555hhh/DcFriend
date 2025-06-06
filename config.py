import os
import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GOOGLE_AI_KEY = os.getenv("GOOGLE_AI_KEY")

if not DISCORD_BOT_TOKEN or not GOOGLE_AI_KEY:
    print("错误：DISCORD_BOT_TOKEN 或 GOOGLE_AI_KEY 未在 .env 文件中设置。", file=sys.stderr)
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "user_data" / "memory.db"
PERSONA_FILE_PATH = BASE_DIR / "prompts" / "persona.json"