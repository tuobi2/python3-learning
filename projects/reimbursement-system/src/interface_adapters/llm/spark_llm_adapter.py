import requests
from src.frameworks.config.settings import Settings

class SparkLLMAdapter:
    """LLM适配器（适配讯飞星火接口）"""
    def __init__(self):
        self.settings = Settings()

    def classify_expense(self, reason: str) -> str:
        """适配LLM接口进行分类"""
        prompt = f"""
你是专业的企业财务报销分类专家，严格按照以下规则分类，仅返回分类名称：
可选类型：交通费、差旅费、业务招待费、办公费、培训费、其他费用

分类优先级：
1. 最高优先级：事由包含「客户、宴请、招待、拜访客户」→ 业务招待费
2. 包含「出差、机票、酒店、差旅」→ 差旅费
3. 纯交通场景（打车、地铁、公交、交通费）且无客户场景 → 交通费
4. 包含「办公用品、设备采购、文具、打印」→ 办公费
5. 包含「员工培训、课程、学习」→ 培训费
6. 其他所有场景 → 其他费用

报销事由：{reason}
输出要求：仅返回分类名称，无其他文字、标点或解释。
        """.strip()

        payload = {
            "model": self.settings.SPARK_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 10
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.settings.SPARK_API_PASSWORD}"
        }

        try:
            response = requests.post(
                self.settings.SPARK_API_URL,
                headers=headers,
                json=payload,
                timeout=15
            )
            response.raise_for_status()
            result = response.json()
            classify_result = result["choices"][0]["message"]["content"].strip()
            valid_types = ["交通费", "差旅费", "业务招待费", "办公费", "培训费", "其他费用"]
            return classify_result if classify_result in valid_types else "其他费用"
        except Exception as e:
            print(f"LLM适配层错误: {e}")
            return "其他费用"
