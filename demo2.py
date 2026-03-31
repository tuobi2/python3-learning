#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能报销审批系统 - 讯飞星火 HTTP 密码鉴权版
适配：https://spark-api-open.xf-yun.com/x2/chat/completions
鉴权方式：SPARK_API_URL + SPARK_API_PASSWORD
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uvicorn
import random
import requests
import sqlite3
from typing import Optional, Dict, Any

# ====================== 核心配置（HTTP 密码鉴权） ======================
app = FastAPI(
    title="智能报销审批系统",
    version="2.0",
    description="基于讯飞星火 HTTP 密码鉴权的智能报销审批服务"
)

# 🔥 HTTP 接口鉴权核心参数（从平台复制）
SPARK_API_URL = "https://spark-api-open.xf-yun.com/x2/chat/completions"  # HTTP接口地址
SPARK_API_PASSWORD = "NXzcWgZZCJKtBoOjYtZJ:RgfvcLDWgRQdIbbijiIS"  # 你的 APIPassword（平台显示的完整值）
SPARK_MODEL = "spark-x"  # 对应 Spark X 模型

# 数据库配置
DB_NAME = "reimbursement.db"

# ====================== 1. 数据库初始化 ======================
def init_database():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS reimbursement_bills (
        bill_id TEXT PRIMARY KEY,
        employee_name TEXT NOT NULL,
        employee_dept TEXT NOT NULL,
        amount REAL NOT NULL,
        expense_type TEXT NOT NULL,
        invoice_num TEXT NOT NULL,
        invoice_date TEXT NOT NULL,
        reason TEXT NOT NULL,
        status TEXT NOT NULL,
        reject_reason TEXT,
        approval_user TEXT,
        create_time TEXT NOT NULL
    )
    """
    cursor.execute(create_table_sql)
    conn.commit()
    return conn

db_conn = init_database()
db_cursor = db_conn.cursor()

# ====================== 2. 讯飞星火 HTTP 密码鉴权工具类 ======================
class SparkLLM:
    """讯飞星火 HTTP 密码鉴权版工具类"""

    @staticmethod
    def expense_classify(reason: str) -> str:
        """
        智能报销费用分类（HTTP 密码鉴权）
        """
        # 精准分类 Prompt
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

        # 请求体
        payload = {
            "model": SPARK_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,  # 低温度保证结果稳定
            "max_tokens": 10     # 仅返回分类名称，限制输出长度
        }

        # 🔥 HTTP 密码鉴权请求头（核心）
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {SPARK_API_PASSWORD}"  # 密码鉴权
        }

        try:
            # 发起 HTTP 请求（无需签名，仅密码鉴权）
            response = requests.post(
                SPARK_API_URL,
                headers=headers,
                json=payload,
                timeout=15
            )
            response.raise_for_status()  # 抛出 HTTP 错误

            # 解析响应
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                classify_result = result["choices"][0]["message"]["content"].strip()
                # 合法性校验
                valid_types = ["交通费", "差旅费", "业务招待费", "办公费", "培训费", "其他费用"]
                return classify_result if classify_result in valid_types else "其他费用"
            return "其他费用"

        except Exception as e:
            print(f"讯飞星火调用失败: {str(e)}")
            return "其他费用"  # 降级策略

# ====================== 3. 发票工具类 ======================
class InvoiceTools:
    """模拟发票 OCR 与验真工具"""
    @staticmethod
    def mock_ocr_extract(image_url: Optional[str] = None) -> Dict[str, Any]:
        """模拟 OCR 提取发票信息"""
        return {
            "invoice_num": f"FP{random.randint(10000000, 99999999)}",
            "invoice_date": datetime.now().strftime("%Y-%m-%d"),
            "amount": round(random.uniform(50, 5000), 2),
            "merchant": f"商户{random.randint(1000, 9999)}"
        }

    @staticmethod
    def mock_tax_verify(invoice_num: str) -> bool:
        """模拟发票验真"""
        return True  # 实际场景对接税务系统

# ====================== 4. 核心业务逻辑 ======================
class ReimbursementAgent:
    """报销审批智能体"""
    def __init__(self):
        self.llm = SparkLLM()
        self.invoice_tools = InvoiceTools()
        # 审批规则
        self.approval_rules = {
            "low": {"max_amount": 500, "approver": "部门经理"},
            "mid": {"max_amount": 3000, "approver": "财务主管"},
            "high": {"max_amount": float("inf"), "approver": "总经理"}
        }
        # 部门预算
        self.dept_budgets = {
            "技术部": 10000.0,
            "财务部": 8000.0,
            "市场部": 15000.0,
            "人事部": 6000.0
        }

    def _generate_bill_id(self) -> str:
        """生成唯一报销单 ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = random.randint(1000, 9999)
        return f"BILL-{timestamp}-{random_suffix}"

    def process_reimbursement(
        self,
        employee_name: str,
        employee_dept: str,
        reason: str,
        invoice_image_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        处理报销申请
        """
        # 1. 提取发票信息
        invoice_info = self.invoice_tools.mock_ocr_extract(invoice_image_url)
        # 2. 智能费用分类
        expense_type = self.llm.expense_classify(reason)

        # 3. 规则校验
        reject_reasons = []
        amount = invoice_info["amount"]

        if amount <= 0:
            reject_reasons.append("报销金额必须大于0")
        if len(invoice_info["invoice_num"]) < 8:
            reject_reasons.append("发票号格式错误（长度不足8位）")
        if employee_dept not in self.dept_budgets:
            reject_reasons.append(f"部门[{employee_dept}]不存在或无预算配置")
        else:
            if amount > self.dept_budgets[employee_dept]:
                reject_reasons.append(
                    f"部门预算不足（{employee_dept}剩余预算：{self.dept_budgets[employee_dept]}元，申请金额：{amount}元）"
                )

        if not self.invoice_tools.mock_tax_verify(invoice_info["invoice_num"]):
            reject_reasons.append("发票验真失败，疑似无效发票")

        # 4. 生成审批结果
        bill_id = self._generate_bill_id()
        create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if reject_reasons:
            status = "已驳回"
            reject_reason = "; ".join(reject_reasons)
            approval_user = None
        else:
            status = "待审批"
            reject_reason = None
            if amount <= self.approval_rules["low"]["max_amount"]:
                approval_user = self.approval_rules["low"]["approver"]
            elif amount <= self.approval_rules["mid"]["max_amount"]:
                approval_user = self.approval_rules["mid"]["approver"]
            else:
                approval_user = self.approval_rules["high"]["approver"]

        # 5. 数据持久化
        insert_sql = """
        INSERT INTO reimbursement_bills
        (bill_id, employee_name, employee_dept, amount, expense_type, invoice_num,
         invoice_date, reason, status, reject_reason, approval_user, create_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        db_cursor.execute(insert_sql, (
            bill_id, employee_name, employee_dept, amount, expense_type,
            invoice_info["invoice_num"], invoice_info["invoice_date"], reason,
            status, reject_reason, approval_user, create_time
        ))
        db_conn.commit()

        return {
            "bill_id": bill_id,
            "employee_name": employee_name,
            "employee_dept": employee_dept,
            "amount": amount,
            "expense_type": expense_type,
            "invoice_num": invoice_info["invoice_num"],
            "status": status,
            "reject_reason": reject_reason,
            "approval_user": approval_user,
            "create_time": create_time
        }

# ====================== 5. API 接口定义 ======================
class ReimbursementRequest(BaseModel):
    employee_name: str
    employee_dept: str
    reason: str
    invoice_image_url: Optional[str] = None

@app.post("/api/reimbursement/submit", summary="提交报销申请")
def submit_reimbursement(request: ReimbursementRequest):
    try:
        agent = ReimbursementAgent()
        result = agent.process_reimbursement(
            employee_name=request.employee_name,
            employee_dept=request.employee_dept,
            reason=request.reason,
            invoice_image_url=request.invoice_image_url
        )
        return {
            "code": 200,
            "message": "报销申请提交成功",
            "data": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"提交失败：{str(e)}"
        )

@app.get("/api/reimbursement/query/{bill_id}", summary="查询报销单详情")
def query_reimbursement(bill_id: str):
    db_cursor.execute(
        "SELECT * FROM reimbursement_bills WHERE bill_id = ?",
        (bill_id,)
    )
    row = db_cursor.fetchone()

    if not row:
        raise HTTPException(
            status_code=404,
            detail=f"报销单ID [{bill_id}] 不存在"
        )

    fields = [
        "bill_id", "employee_name", "employee_dept", "amount", "expense_type",
        "invoice_num", "invoice_date", "reason", "status", "reject_reason",
        "approval_user", "create_time"
    ]

    return {
        "code": 200,
        "message": "查询成功",
        "data": dict(zip(fields, row))
    }

@app.get("/api/reimbursement/health", summary="服务健康检查")
def health_check():
    return {
        "code": 200,
        "message": "服务运行正常",
        "data": {
            "service": "reimbursement-agent",
            "status": "running",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "llm": "讯飞星火 Spark X HTTP 密码鉴权版"
        }
    }

# ====================== 6. 启动服务 ======================
def main():
    print("=" * 60)
    print("智能报销审批系统 - 讯飞星火 HTTP 密码鉴权版")
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API地址: {SPARK_API_URL}")
    print("=" * 60)
    print("服务地址: http://127.0.0.1:8000")
    print("API文档: http://127.0.0.1:8000/docs")
    print("=" * 60)

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=False  # 生产环境建议关闭热重载
    )

if __name__ == "__main__":
    main()
