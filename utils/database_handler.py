# utils/database_handler.py
import sqlite3
import config  # 我们需要从 config 模块导入数据库路径
from pathlib import Path

def get_db_connection():
    """获取并返回一个数据库连接对象。"""
    # 使用 Path 对象来处理路径，更健壮
    db_path = Path(config.DATABASE_PATH)
    # 确保父目录（user_data/）存在
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 连接到数据库
    conn = sqlite3.connect(db_path)
    # 设置 row_factory，这样查询结果可以像字典一样通过列名访问
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    初始化数据库。如果表不存在，就创建它们。
    这是一个幂等操作，可以安全地多次运行。
    """
    print("正在初始化数据库...")
    try:
        # 使用 'with' 语句确保连接在使用后能被正确关闭
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # 创建 'events' 表，用于记录所有对话事件
            # 使用 TEXT/INTEGER/REAL/BLOB/NULL 作为列类型
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER NOT NULL,
                    user_name TEXT NOT NULL,
                    role TEXT NOT NULL, -- 'user' 或 'model'
                    content TEXT NOT NULL
                )
            ''')
            
            # 创建 'members' 表，用于记录社团成员信息
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS members (
                    user_id INTEGER PRIMARY KEY,
                    user_name TEXT NOT NULL,
                    first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT
                )
            ''')
            
            # 提交事务，将更改写入数据库文件
            conn.commit()
        print("数据库初始化成功。")
        return True
    except sqlite3.Error as e:
        # 如果发生任何数据库错误，打印出来
        print(f"数据库初始化失败：{e}")
        return False