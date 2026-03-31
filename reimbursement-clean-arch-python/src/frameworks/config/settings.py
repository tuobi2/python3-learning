from dataclasses import dataclass

@dataclass
class Settings:
    """配置类（框架层）"""
    # LLM配置
    SPARK_API_URL: str = "https://spark-api-open.xf-yun.com/x2/chat/completions"
    SPARK_API_PASSWORD: str = "NXzcWgZZCJKtBoOjYtZJ:RgfvcLDWgRQdIbbijiIS"  # 替换为实际值
    SPARK_MODEL: str = "spark-x"
    
    # 数据库配置
    DB_NAME: str = "reimbursement_clean_arch.db"
    
    # 服务器配置
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
