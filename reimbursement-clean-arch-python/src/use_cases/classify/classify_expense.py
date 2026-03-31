from typing import Optional
from src.interface_adapters.llm.spark_llm_adapter import SparkLLMAdapter

class ClassifyExpenseUseCase:
    """分类用例（智能体核心逻辑）"""
    def __init__(self, llm_adapter: Optional[SparkLLMAdapter] = None):
        self.llm_adapter = llm_adapter or SparkLLMAdapter()

    def execute(self, reason: str) -> str:
        """执行分类"""
        return self.llm_adapter.classify_expense(reason)
