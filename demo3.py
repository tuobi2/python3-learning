#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报销审批多智能体系统（Multi-Agent）
架构：调度 + 分类 + 审核 + 财务 + 通知 五大智能体
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uvicorn
import random
import requests
import sqlite3
from typing import Optional, Dict, Any, Tuple

# ====================== 核心配置 ======================
app = FastAPI(
    title="报销审批多智能体系统",
    version="3.0",
    description="基于讯飞星火的企业级多智能体报销审批服务"
)

# 讯飞星火 HTTP 配置
SPARK_API_URL = "https://spark-api-open.xf-yun.com/x2/chat/completions"
SPARK_API_PASSWORD = "NXzcWgZZCJKtBoOjYtZJ:RgfvcLDWgRQdIbbijiIS"  # 替换为实际值
SPARK_MODEL = "spark-x"

# 数据库配置
DB_NAME = "reimbursement_multi_agent.db"

# ====================== 1. 基础工具类 ======================
class DatabaseTool:
    """数据库工具（所有智能体共用）"""
    @staticmethod
    def init_db():
        """初始化数据库（新增通知记录表）"""
        conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        cursor = conn.cursor()

        # 报销单表
        cursor.execute("""
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
            audit_reason TEXT,
            approval_user TEXT,
            create_time TEXT NOT NULL,
            update_time TEXT NOT NULL
        )
        """)

        # 通知记录表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS notification_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id TEXT NOT NULL,
            employee_name TEXT NOT NULL,
            message TEXT NOT NULL,
            notify_time TEXT NOT NULL,
            FOREIGN KEY (bill_id) REFERENCES reimbursement_bills(bill_id)
        )
        """)
        conn.commit()
        return conn

    @staticmethod
    def insert_bill(bill_data: Dict[str, Any]):
        """插入报销单"""
        conn = DatabaseTool.init_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO reimbursement_bills
        (bill_id, employee_name, employee_dept, amount, expense_type, invoice_num,
         invoice_date, reason, status, audit_reason, approval_user, create_time, update_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            bill_data["bill_id"], bill_data["employee_name"], bill_data["employee_dept"],
            bill_data["amount"], bill_data["expense_type"], bill_data["invoice_num"],
            bill_data["invoice_date"], bill_data["reason"], bill_data["status"],
            bill_data["audit_reason"], bill_data["approval_user"],
            bill_data["create_time"], bill_data["update_time"]
        ))
        conn.commit()

    @staticmethod
    def insert_notification(notify_data: Dict[str, Any]):
        """插入通知记录"""
        conn = DatabaseTool.init_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO notification_records
        (bill_id, employee_name, message, notify_time)
        VALUES (?, ?, ?, ?)
        """, (
            notify_data["bill_id"], notify_data["employee_name"],
            notify_data["message"], notify_data["notify_time"]
        ))
        conn.commit()

class InvoiceTool:
    """发票工具类"""
    @staticmethod
    def extract_invoice_info(image_url: Optional[str] = None) -> Dict[str, Any]:
        """模拟OCR提取发票信息"""
        return {
            "invoice_num": f"FP{random.randint(10000000, 99999999)}",
            "invoice_date": datetime.now().strftime("%Y-%m-%d"),
            "amount": round(random.uniform(50, 5000), 2),
            "merchant": f"商户{random.randint(1000, 9999)}"
        }

    @staticmethod
    def verify_invoice(invoice_num: str) -> bool:
        """模拟发票验真"""
        return True  # 实际对接税务系统

# ====================== 2. 核心智能体定义 ======================
class ClassifyAgent:
    """分类智能体：负责费用类型识别"""
    def __init__(self):
        self.name = "分类智能体"

    def classify_expense(self, reason: str) -> str:
        """调用LLM进行费用分类"""
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
            "model": SPARK_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 10
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {SPARK_API_PASSWORD}"
        }

        try:
            response = requests.post(SPARK_API_URL, headers=headers, json=payload, timeout=15)
            response.raise_for_status()
            result = response.json()
            classify_result = result["choices"][0]["message"]["content"].strip()
            valid_types = ["交通费", "差旅费", "业务招待费", "办公费", "培训费", "其他费用"]
            return classify_result if classify_result in valid_types else "其他费用"
        except Exception as e:
            print(f"{self.name}调用失败: {e}")
            return "其他费用"

class AuditAgent:
    """审核智能体：负责规则校验与审批人分配"""
    def __init__(self):
        self.name = "审核智能体"
        # 审批规则配置
        self.approval_rules = {
            "low": {"max_amount": 500, "approver": "部门经理"},
            "mid": {"max_amount": 3000, "approver": "财务主管"},
            "high": {"max_amount": float("inf"), "approver": "总经理"}
        }
        # 部门预算配置
        self.dept_budgets = {
            "技术部": 10000.0,
            "财务部": 8000.0,
            "市场部": 15000.0,
            "人事部": 6000.0
        }

    def audit_reimbursement(self, dept: str, amount: float, invoice_num: str) -> Tuple[bool, str, Optional[str]]:
        """
        审核报销申请
        返回：(是否通过, 审核原因, 审批人)
        """
        # 规则校验
        reject_reasons = []
        if amount <= 0:
            reject_reasons.append("报销金额必须大于0")
        if len(invoice_num) < 8:
            reject_reasons.append("发票号格式错误（长度不足8位）")
        if dept not in self.dept_budgets:
            reject_reasons.append(f"部门[{dept}]不存在或无预算配置")
        else:
            if amount > self.dept_budgets[dept]:
                reject_reasons.append(f"部门预算不足（{dept}剩余预算：{self.dept_budgets[dept]}元，申请金额：{amount}元）")
        if not InvoiceTool.verify_invoice(invoice_num):
            reject_reasons.append("发票验真失败，疑似无效发票")

        # 审核结果
        if reject_reasons:
            return False, "; ".join(reject_reasons), None

        # 分配审批人
        if amount <= self.approval_rules["low"]["max_amount"]:
            approver = self.approval_rules["low"]["approver"]
        elif amount <= self.approval_rules["mid"]["max_amount"]:
            approver = self.approval_rules["mid"]["approver"]
        else:
            approver = self.approval_rules["high"]["approver"]

        return True, "审核通过", approver

class FinanceAgent:
    """财务智能体：负责生成报销单与财务处理"""
    def __init__(self):
        self.name = "财务智能体"

    def generate_bill(self, name: str, dept: str, reason: str, amount: float, expense_type: str, invoice_info: Dict[str, Any]) -> Dict[str, Any]:
        """生成报销单"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        bill_id = f"BILL-{timestamp}-{random.randint(1000, 9999)}"
        create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "bill_id": bill_id,
            "employee_name": name,
            "employee_dept": dept,
            "amount": amount,
            "expense_type": expense_type,
            "invoice_num": invoice_info["invoice_num"],
            "invoice_date": invoice_info["invoice_date"],
            "reason": reason,
            "status": "待审批",
            "audit_reason": "",
            "approval_user": "",
            "create_time": create_time,
            "update_time": create_time
        }

class NotifyAgent:
    """通知智能体：负责结果通知"""
    def __init__(self):
        self.name = "通知智能体"

    def send_notification(self, bill_id: str, name: str, is_pass: bool, reason: str, approver: Optional[str] = None) -> Dict[str, Any]:
        """发送通知（模拟短信/邮件）"""
        notify_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if is_pass:
            message = f"【报销审批通知】你的报销单（ID：{bill_id}）已通过审核，审批人：{approver}，请等待打款。"
        else:
            message = f"【报销审批通知】你的报销单（ID：{bill_id}）已被驳回，原因：{reason}，请修改后重新提交。"

        # 插入通知记录
        notify_data = {
            "bill_id": bill_id,
            "employee_name": name,
            "message": message,
            "notify_time": notify_time
        }
        DatabaseTool.insert_notification(notify_data)

        # 模拟发送通知
        print(f"{self.name}发送通知给{name}：{message}")
        return notify_data

class DispatcherAgent:
    """调度智能体：核心调度，协调所有智能体工作"""
    def __init__(self):
        self.name = "调度智能体"
        self.classify_agent = ClassifyAgent()
        self.audit_agent = AuditAgent()
        self.finance_agent = FinanceAgent()
        self.notify_agent = NotifyAgent()

    def process_reimbursement(self, name: str, dept: str, reason: str, img_url: Optional[str] = None) -> Dict[str, Any]:
        """
        调度所有智能体完成报销流程
        """
        print(f"{self.name}开始处理{name}的报销请求...")

        # 1. 调用发票工具提取信息
        invoice_info = InvoiceTool.extract_invoice_info(img_url)
        amount = invoice_info["amount"]

        # 2. 调用分类智能体
        expense_type = self.classify_agent.classify_expense(reason)
        print(f"{self.classify_agent.name}识别费用类型：{expense_type}")

        # 3. 调用审核智能体
        is_pass, audit_reason, approver = self.audit_agent.audit_reimbursement(dept, amount, invoice_info["invoice_num"])
        print(f"{self.audit_agent.name}审核结果：{'通过' if is_pass else '驳回'}，原因：{audit_reason}")

        # 4. 调用财务智能体生成报销单
        bill_data = self.finance_agent.generate_bill(name, dept, reason, amount, expense_type, invoice_info)
        bill_data["status"] = "已通过" if is_pass else "已驳回"
        bill_data["audit_reason"] = audit_reason
        bill_data["approval_user"] = approver if is_pass else ""
        bill_data["update_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 5. 保存报销单
        DatabaseTool.insert_bill(bill_data)

        # 6. 调用通知智能体
        self.notify_agent.send_notification(bill_data["bill_id"], name, is_pass, audit_reason, approver)

        # 返回最终结果
        return {
            "bill_id": bill_data["bill_id"],
            "employee_name": name,
            "employee_dept": dept,
            "amount": amount,
            "expense_type": expense_type,
            "status": bill_data["status"],
            "audit_reason": audit_reason,
            "approval_user": approver,
            "message": "报销流程处理完成，结果已通知"
        }

# ====================== 3. API 接口 ======================
class ReimbursementRequest(BaseModel):
    employee_name: str
    employee_dept: str
    reason: str
    invoice_image_url: Optional[str] = None

@app.post("/api/reimbursement/submit", summary="提交报销申请（多智能体版）")
def submit_reimbursement(request: ReimbursementRequest):
    try:
        # 初始化调度智能体
        dispatcher = DispatcherAgent()
        result = dispatcher.process_reimbursement(
            request.employee_name,
            request.employee_dept,
            request.reason,
            request.invoice_image_url
        )
        return {
            "code": 200,
            "message": "报销申请提交成功（多智能体处理完成）",
            "data": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"提交失败：{str(e)}"
        )

@app.get("/api/reimbursement/query/{bill_id}", summary="查询报销单详情")
def query_reimbursement(bill_id: str):
    conn = DatabaseTool.init_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reimbursement_bills WHERE bill_id = ?", (bill_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail=f"报销单ID [{bill_id}] 不存在")

    fields = [
        "bill_id", "employee_name", "employee_dept", "amount", "expense_type",
        "invoice_num", "invoice_date", "reason", "status", "audit_reason",
        "approval_user", "create_time", "update_time"
    ]
    bill_data = dict(zip(fields, row))

    # 查询通知记录
    cursor.execute("SELECT message FROM notification_records WHERE bill_id = ?", (bill_id,))
    notify_row = cursor.fetchone()
    bill_data["notification"] = notify_row[0] if notify_row else "暂无通知"

    return {
        "code": 200,
        "message": "查询成功",
        "data": bill_data
    }

@app.get("/api/health", summary="服务健康检查")
def health_check():
    return {
        "code": 200,
        "message": "多智能体报销系统运行正常",
        "data": {
            "agents": ["调度智能体", "分类智能体", "审核智能体", "财务智能体", "通知智能体"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }

# ====================== 4. 启动服务 ======================
if __name__ == "__main__":
    # 初始化数据库
    DatabaseTool.init_db()
    print("=" * 60)
    print("报销审批多智能体系统（Multi-Agent）启动成功！")
    print("服务地址: http://127.0.0.1:8000")
    print("API文档: http://127.0.0.1:8000/docs")
    print("=" * 60)
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
