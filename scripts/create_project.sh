#!/bin/bash

# 项目名称
PROJECT_NAME="reimbursement-clean-arch-python"

# ====================== 创建目录结构 ======================
mkdir -p ${PROJECT_NAME}/src/{domain/{entities,value_objects},use_cases/{classify,audit,finance,notify,dispatcher},interface_adapters/{repositories,llm,invoice},frameworks/{api,config}}
touch ${PROJECT_NAME}/{main.py,requirements.txt,.gitignore}

# ====================== 生成requirements.txt ======================
cat > ${PROJECT_NAME}/requirements.txt << 'EOF'
fastapi>=0.110.0
uvicorn>=0.29.0
requests>=2.31.0
python-dotenv>=1.0.1
pydantic>=2.6.4
sqlite3>=2.6.0
typing-extensions>=4.10.0
EOF

# ====================== 生成.gitignore ======================
cat > ${PROJECT_NAME}/.gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg
ENV/

# Environment variables
.env
.venv
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Logs
logs/
*.log

# Database
*.db
*.sqlite3
EOF

# ====================== 生成实体层：bill.py ======================
cat > ${PROJECT_NAME}/src/domain/entities/bill.py << 'EOF'
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass(frozen=False)
class ReimbursementBill:
    """报销单实体（核心业务对象）"""
    bill_id: str
    employee_name: str
    employee_dept: str
    amount: float
    expense_type: str
    invoice_num: str
    invoice_date: str
    reason: str
    status: str
    audit_reason: Optional[str] = None
    approval_user: Optional[str] = None
    create_time: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    update_time: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # 业务规则封装（实体自己的行为）
    def is_approved(self) -> bool:
        return self.status == "已通过"
    
    def is_rejected(self) -> bool:
        return self.status == "已驳回"
    
    def update_status(self, status: str, audit_reason: Optional[str] = None) -> 'ReimbursementBill':
        """更新状态"""
        self.status = status
        self.audit_reason = audit_reason or self.audit_reason
        self.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self
EOF

# ====================== 生成实体层：notification.py ======================
cat > ${PROJECT_NAME}/src/domain/entities/notification.py << 'EOF'
from dataclasses import dataclass, field
from datetime import datetime

@dataclass(frozen=False)
class Notification:
    """通知实体"""
    bill_id: str
    employee_name: str
    message: str
    notify_time: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
EOF

# ====================== 生成配置文件：settings.py ======================
cat > ${PROJECT_NAME}/src/frameworks/config/settings.py << 'EOF'
from dataclasses import dataclass

@dataclass
class Settings:
    """配置类（框架层）"""
    # LLM配置
    SPARK_API_URL: str = "https://spark-api-open.xf-yun.com/x2/chat/completions"
    SPARK_API_PASSWORD: str = "你的APIPassword"  # 替换为实际值
    SPARK_MODEL: str = "spark-x"
    
    # 数据库配置
    DB_NAME: str = "reimbursement_clean_arch.db"
    
    # 服务器配置
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
EOF

# ====================== 生成LLM适配器：spark_llm_adapter.py ======================
cat > ${PROJECT_NAME}/src/interface_adapters/llm/spark_llm_adapter.py << 'EOF'
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
EOF

# ====================== 生成数据库适配器：bill_repository.py ======================
cat > ${PROJECT_NAME}/src/interface_adapters/repositories/bill_repository.py << 'EOF'
import sqlite3
from typing import Optional, List
from src.domain.entities.bill import ReimbursementBill
from src.frameworks.config.settings import Settings

class BillRepository:
    """报销单仓库（数据库适配器）"""
    def __init__(self):
        self.settings = Settings()
        self._init_db()

    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.settings.DB_NAME, check_same_thread=False)
        cursor = conn.cursor()
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
        conn.commit()
        conn.close()

    def save(self, bill: ReimbursementBill):
        """保存报销单"""
        conn = sqlite3.connect(self.settings.DB_NAME, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO reimbursement_bills 
        (bill_id, employee_name, employee_dept, amount, expense_type, invoice_num, 
         invoice_date, reason, status, audit_reason, approval_user, create_time, update_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            bill.bill_id, bill.employee_name, bill.employee_dept,
            bill.amount, bill.expense_type, bill.invoice_num,
            bill.invoice_date, bill.reason, bill.status,
            bill.audit_reason, bill.approval_user,
            bill.create_time, bill.update_time
        ))
        conn.commit()
        conn.close()

    def get_by_id(self, bill_id: str) -> Optional[ReimbursementBill]:
        """根据ID查询报销单"""
        conn = sqlite3.connect(self.settings.DB_NAME, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reimbursement_bills WHERE bill_id = ?", (bill_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return ReimbursementBill(
            bill_id=row[0],
            employee_name=row[1],
            employee_dept=row[2],
            amount=row[3],
            expense_type=row[4],
            invoice_num=row[5],
            invoice_date=row[6],
            reason=row[7],
            status=row[8],
            audit_reason=row[9],
            approval_user=row[10],
            create_time=row[11],
            update_time=row[12]
        )
EOF

# ====================== 生成用例层：classify_expense.py ======================
cat > ${PROJECT_NAME}/src/use_cases/classify/classify_expense.py << 'EOF'
from typing import Optional
from src.interface_adapters.llm.spark_llm_adapter import SparkLLMAdapter

class ClassifyExpenseUseCase:
    """分类用例（智能体核心逻辑）"""
    def __init__(self, llm_adapter: Optional[SparkLLMAdapter] = None):
        self.llm_adapter = llm_adapter or SparkLLMAdapter()

    def execute(self, reason: str) -> str:
        """执行分类"""
        return self.llm_adapter.classify_expense(reason)
EOF

# ====================== 生成用例层：audit_reimbursement.py ======================
cat > ${PROJECT_NAME}/src/use_cases/audit/audit_reimbursement.py << 'EOF'
from typing import Tuple, Optional
from src.interface_adapters.invoice.invoice_adapter import InvoiceAdapter

class AuditReimbursementUseCase:
    """审核用例"""
    def __init__(self, invoice_adapter: Optional[InvoiceAdapter] = None):
        self.invoice_adapter = invoice_adapter or InvoiceAdapter()
        # 审批规则（业务规则封装在UseCase）
        self.approval_rules = {
            "low": {"max_amount": 500, "approver": "部门经理"},
            "mid": {"max_amount": 3000, "approver": "财务主管"},
            "high": {"max_amount": float("inf"), "approver": "总经理"}
        }
        self.dept_budgets = {
            "技术部": 10000.0,
            "财务部": 8000.0,
            "市场部": 15000.0,
            "人事部": 6000.0
        }

    def execute(self, dept: str, amount: float, invoice_num: str) -> Tuple[bool, str, Optional[str]]:
        """执行审核"""
        reject_reasons = []
        
        # 业务规则校验
        if amount <= 0:
            reject_reasons.append("报销金额必须大于0")
        if len(invoice_num) < 8:
            reject_reasons.append("发票号格式错误（长度不足8位）")
        if dept not in self.dept_budgets:
            reject_reasons.append(f"部门[{dept}]不存在或无预算配置")
        else:
            if amount > self.dept_budgets[dept]:
                reject_reasons.append(f"部门预算不足（{dept}剩余预算：{self.dept_budgets[dept]}元，申请金额：{amount}元）")
        if not self.invoice_adapter.verify_invoice(invoice_num):
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
EOF

# ====================== 生成FastAPI接口：fastapi_app.py ======================
cat > ${PROJECT_NAME}/src/frameworks/api/fastapi_app.py << 'EOF'
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from src.use_cases.dispatcher.process_reimbursement import ProcessReimbursementUseCase
from src.frameworks.config.settings import Settings

# 初始化配置
settings = Settings()

# 初始化FastAPI应用
app = FastAPI(
    title="报销审批系统（Clean Architecture版）",
    version="4.0",
    description="基于Bob大叔Clean Architecture的企业级多智能体系统"
)

# 请求模型
class ReimbursementRequest(BaseModel):
    employee_name: str
    employee_dept: str
    reason: str
    invoice_image_url: Optional[str] = None

# 响应模型
class ReimbursementResponse(BaseModel):
    code: int
    message: str
    data: Optional[dict] = None

# API接口
@app.post("/api/reimbursement/submit", response_model=ReimbursementResponse, summary="提交报销申请")
def submit_reimbursement(request: ReimbursementRequest):
    try:
        use_case = ProcessReimbursementUseCase()
        result = use_case.execute(
            employee_name=request.employee_name,
            employee_dept=request.employee_dept,
            reason=request.reason,
            invoice_image_url=request.invoice_image_url
        )
        return ReimbursementResponse(
            code=200,
            message="报销申请提交成功（Clean Architecture处理完成）",
            data=result
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"提交失败：{str(e)}"
        )

@app.get("/api/reimbursement/query/{bill_id}", response_model=ReimbursementResponse, summary="查询报销单详情")
def query_reimbursement(bill_id: str):
    from src.interface_adapters.repositories.bill_repository import BillRepository
    repo = BillRepository()
    bill = repo.get_by_id(bill_id)
    
    if not bill:
        raise HTTPException(status_code=404, detail=f"报销单ID [{bill_id}] 不存在")
    
    return ReimbursementResponse(
        code=200,
        message="查询成功",
        data={
            "bill_id": bill.bill_id,
            "employee_name": bill.employee_name,
            "employee_dept": bill.employee_dept,
            "amount": bill.amount,
            "expense_type": bill.expense_type,
            "status": bill.status,
            "audit_reason": bill.audit_reason,
            "approval_user": bill.approval_user,
            "create_time": bill.create_time,
            "update_time": bill.update_time
        }
    )

@app.get("/api/health", response_model=ReimbursementResponse, summary="服务健康检查")
def health_check():
    return ReimbursementResponse(
        code=200,
        message="Clean Architecture报销系统运行正常",
        data={
            "architecture": "Bob大叔Clean Architecture（四层架构）",
            "principles": "SOLID (SRP, OCP, LSP, ISP, DIP)",
            "timestamp": "2026-03-15 18:00:00"
        }
    )
EOF

# ====================== 生成启动入口：main.py ======================
cat > ${PROJECT_NAME}/main.py << 'EOF'
from src.frameworks.api.fastapi_app import app, settings
import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("报销审批系统（Bob大叔Clean Architecture版）启动成功！")
    print("架构：Entities → Use Cases → Interface Adapters → Frameworks & Drivers")
    print("原则：SOLID (SRP为首)")
    print(f"服务地址: http://{settings.API_HOST}:{settings.API_PORT}")
    print(f"API文档: http://{settings.API_HOST}:{settings.API_PORT}/docs")
    print("=" * 60)
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT, reload=False)
EOF

# ====================== 补充其他核心文件（简化版） ======================
# 发票适配器
cat > ${PROJECT_NAME}/src/interface_adapters/invoice/invoice_adapter.py << 'EOF'
import random

class InvoiceAdapter:
    """发票工具适配器"""
    def extract_invoice_info(self, image_url: str = None) -> dict:
        """模拟OCR提取发票信息"""
        return {
            "invoice_num": f"FP{random.randint(10000000, 99999999)}",
            "invoice_date": "2026-03-15",
            "amount": round(random.uniform(50, 5000), 2),
            "merchant": f"商户{random.randint(1000, 9999)}"
        }
    
    def verify_invoice(self, invoice_num: str) -> bool:
        """模拟发票验真"""
        return True
EOF

# 调度用例
cat > ${PROJECT_NAME}/src/use_cases/dispatcher/process_reimbursement.py << 'EOF'
import random
from datetime import datetime
from src.use_cases.classify.classify_expense import ClassifyExpenseUseCase
from src.use_cases.audit.audit_reimbursement import AuditReimbursementUseCase
from src.interface_adapters.invoice.invoice_adapter import InvoiceAdapter
from src.interface_adapters.repositories.bill_repository import BillRepository
from src.domain.entities.bill import ReimbursementBill

class ProcessReimbursementUseCase:
    """调度用例（核心调度）"""
    def __init__(self):
        self.classify_use_case = ClassifyExpenseUseCase()
        self.audit_use_case = AuditReimbursementUseCase()
        self.invoice_adapter = InvoiceAdapter()
        self.bill_repository = BillRepository()

    def execute(self, employee_name: str, employee_dept: str, reason: str, invoice_image_url: str = None) -> dict:
        """执行完整报销流程"""
        # 1. 提取发票信息
        invoice_info = self.invoice_adapter.extract_invoice_info(invoice_image_url)
        amount = invoice_info["amount"]
        
        # 2. 费用分类
        expense_type = self.classify_use_case.execute(reason)
        
        # 3. 审核报销
        is_pass, audit_reason, approver = self.audit_use_case.execute(
            dept=employee_dept,
            amount=amount,
            invoice_num=invoice_info["invoice_num"]
        )
        
        # 4. 生成报销单
        bill_id = f"BILL-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"
        bill = ReimbursementBill(
            bill_id=bill_id,
            employee_name=employee_name,
            employee_dept=employee_dept,
            amount=amount,
            expense_type=expense_type,
            invoice_num=invoice_info["invoice_num"],
            invoice_date=invoice_info["invoice_date"],
            reason=reason,
            status="已通过" if is_pass else "已驳回",
            audit_reason=audit_reason,
            approval_user=approver or ""
        )
        
        # 5. 保存报销单
        self.bill_repository.save(bill)
        
        # 返回结果
        return {
            "bill_id": bill_id,
            "employee_name": employee_name,
            "expense_type": expense_type,
            "amount": amount,
            "status": bill.status,
            "audit_reason": audit_reason,
            "approval_user": approver or ""
        }

    def query_bill(self, bill_id: str) -> dict:
        """查询报销单"""
        bill = self.bill_repository.get_by_id(bill_id)
        if not bill:
            raise Exception(f"报销单ID {bill_id} 不存在")
        
        return {
            "bill_id": bill.bill_id,
            "employee_name": bill.employee_name,
            "employee_dept": bill.employee_dept,
            "amount": bill.amount,
            "expense_type": bill.expense_type,
            "status": bill.status,
            "audit_reason": bill.audit_reason,
            "approval_user": bill.approval_user,
            "create_time": bill.create_time,
            "update_time": bill.update_time
        }
EOF

echo "✅ Python Clean Architecture项目生成完成！"
echo "📁 项目目录：${PROJECT_NAME}"
echo "🚀 快速启动："
echo "   cd ${PROJECT_NAME}"
echo "   pip install -r requirements.txt"
echo "   python main.py"
echo "🔍 访问API文档：http://0.0.0.0:8000/docs"