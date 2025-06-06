# utils/database_handler.py (最终正确版本)
import sqlite3
import config
from pathlib import Path
from datetime import datetime

def get_db_connection():
    """获取并返回一个数据库连接对象。"""
    db_path = Path(config.DATABASE_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化数据库，创建所有必要的表。"""
    print("数据库检查/初始化完成。") # 简化日志
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER NOT NULL,
                    user_name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS members (
                    user_id INTEGER PRIMARY KEY,
                    user_name TEXT NOT NULL,
                    first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT
                )
            ''')
            conn.commit()
    except sqlite3.Error as e:
        print(f"数据库初始化时发生错误：{e}")

def add_dialogue_event(user_id: int, user_name: str, role: str, content: str):
    """向数据库中添加一条对话事件，并检查/添加成员。"""
    try:
        with get_db_connection() as conn:
            timestamp = datetime.now()
            # 插入对话事件
            conn.execute(
                "INSERT INTO events (timestamp, user_id, user_name, role, content) VALUES (?, ?, ?, ?, ?)",
                (timestamp, user_id, user_name, role, content)
            )
            
            # 检查成员是否存在
            member = conn.execute("SELECT user_id FROM members WHERE user_id = ?", (user_id,)).fetchone()
            if not member:
                # 如果不存在，则插入新成员
                conn.execute(
                    "INSERT INTO members (user_id, user_name, first_seen) VALUES (?, ?, ?)",
                    (user_id, user_name, timestamp)
                )
            
            conn.commit()
    except sqlite3.Error as e:
        print(f"记录对话事件时发生错误：{e}")

def get_recent_dialogue(limit: int = 10) -> list[dict]:
    """获取最近的对话历史。"""
    try:
        with get_db_connection() as conn:
            rows = conn.execute(
                "SELECT user_name, role, content FROM events ORDER BY timestamp DESC LIMIT ?", 
                (limit,)
            ).fetchall()
            # 将查询结果（倒序）反转为正序，并转换为字典列表
            return list(reversed([dict(row) for row in rows]))
    except sqlite3.Error as e:
        print(f"获取对话历史时发生错误：{e}")
        return [] # 如果出错，返回空列表