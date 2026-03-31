from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import random
# 导入uvicorn的Config和Server类（替代直接run）
import uvicorn
from uvicorn.config import Config
from uvicorn.server import Server

# 初始化 FastAPI 应用
app = FastAPI(title="智能报销审批 Demo", version="1.0")

# ====================== 模拟数据与核心模型 ======================
# 1. 报销单状态枚举
class ReimbursementStatus:
    DRAFT = "草稿"          # 初始状态
    PENDING_REVIEW = "待初审" # 提交后待智能初审
    PENDING_APPROVAL = "待审批" # 初审通过待人工审批
    APPROVED = "已通过"      # 审批完成
    REJECTED = "已驳回"      # 初审/审批驳回
    ARCHIVED = "已归档"      # 付款后归档

# 2. 报销单数据模型
class ReimbursementBill(BaseModel):
    bill_id: str = None                # 报销单ID（自动生成）
    employee_name: str                 # 员工姓名
    employee_dept: str                 # 所属部门
    amount: float                      # 报销金额
    expense_type: str = None           # 费用类型（AI自动匹配）
    invoice_num: str                   # 发票号
    invoice_date: str                  # 发票日期
    reason: str                        # 报销事由
    status: str = ReimbursementStatus.DRAFT  # 状态
    reject_reason: str = None          # 驳回原因
    approval_user: str = None          # 审批人
    create_time: str = None            # 创建时间

# 3. 模拟数据库（存储报销单）
bill_database = {}
# 4. 模拟费用类型匹配规则（AI 语义理解简化版）
expense_type_rules = {
    "打车": "交通费",
    "机票": "差旅费",
    "酒店": "差旅费",
    "餐饮": "业务招待费",
    "办公用品": "办公费",
    "培训": "培训费",
    "快递": "办公费"
}
# 5. 模拟审批权限规则
approval_rules = {
    "low": {"max_amount": 500, "approver": "部门经理"},
    "mid": {"max_amount": 3000, "approver": "财务主管"},
    "high": {"max_amount": float("inf"), "approver": "总经理"}
}

# ====================== 核心功能函数（AI 智能体逻辑） ======================
# 1. AI 填单智能体：自动生成报销单ID、匹配费用类型、记录创建时间
def ai_fill_bill(bill: ReimbursementBill) -> ReimbursementBill:
    # 自动生成报销单ID（时间戳+随机数）
    bill.bill_id = f"BILL-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"
    # AI 匹配费用类型（模拟语义理解）
    for keyword, type_name in expense_type_rules.items():
        if keyword in bill.reason:
            bill.expense_type = type_name
            break
    if not bill.expense_type:
        bill.expense_type = "其他费用"
    # 记录创建时间
    bill.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 状态改为待初审
    bill.status = ReimbursementStatus.PENDING_REVIEW
    return bill

# 2. 规则智能体：智能初审（校验发票、金额、预算等）
def ai_review_bill(bill: ReimbursementBill) -> ReimbursementBill:
    # 模拟校验逻辑
    reject_reason = []
    # 校验1：发票号格式（简单校验）
    if len(bill.invoice_num) < 8:
        reject_reason.append("发票号格式错误（长度不足8位）")
    # 校验2：报销金额是否为正数
    if bill.amount <= 0:
        reject_reason.append("报销金额必须大于0")
    # 校验3：模拟预算校验（部门预算充足）
    dept_budget = {"技术部": 10000, "财务部": 8000, "市场部": 15000}
    if bill.employee_dept not in dept_budget:
        reject_reason.append("部门不存在，无预算信息")
    elif bill.amount > dept_budget[bill.employee_dept]:
        reject_reason.append(f"部门预算不足（剩余预算：{dept_budget[bill.employee_dept]}元）")
    
    # 根据校验结果更新状态
    if reject_reason:
        bill.status = ReimbursementStatus.REJECTED
        bill.reject_reason = "; ".join(reject_reason)
    else:
        bill.status = ReimbursementStatus.PENDING_APPROVAL
        # 自动匹配审批人
        if bill.amount <= approval_rules["low"]["max_amount"]:
            bill.approval_user = approval_rules["low"]["approver"]
        elif bill.amount <= approval_rules["mid"]["max_amount"]:
            bill.approval_user = approval_rules["mid"]["approver"]
        else:
            bill.approval_user = approval_rules["high"]["approver"]
    return bill

# 3. 流程智能体：人工审批（模拟）
def manual_approve(bill_id: str, approve: bool, approver_name: str) -> ReimbursementBill:
    if bill_id not in bill_database:
        raise HTTPException(status_code=404, detail="报销单不存在")
    bill = bill_database[bill_id]
    if bill.status != ReimbursementStatus.PENDING_APPROVAL:
        raise HTTPException(status_code=400, detail="当前报销单不处于待审批状态")
    
    if approve:
        bill.status = ReimbursementStatus.APPROVED
        # 审批通过后自动归档
        bill.status = ReimbursementStatus.ARCHIVED
    else:
        bill.status = ReimbursementStatus.REJECTED
        bill.reject_reason = "人工审批驳回"
    return bill

# ====================== API 接口（供前端/测试调用） ======================
# 1. 提交报销单（AI 填单 + 智能初审）
@app.post("/submit_bill", response_model=ReimbursementBill)
def submit_bill(bill: ReimbursementBill):
    # AI 自动填单
    filled_bill = ai_fill_bill(bill)
    # AI 智能初审
    reviewed_bill = ai_review_bill(filled_bill)
    # 存入数据库
    bill_database[filled_bill.bill_id] = reviewed_bill
    return reviewed_bill

# 2. 人工审批报销单
@app.post("/approve_bill/{bill_id}")
def approve_bill(bill_id: str, approve: bool = True, approver_name: str = "默认审批人"):
    try:
        result = manual_approve(bill_id, approve, approver_name)
        return {"message": "审批完成", "bill": result}
    except HTTPException as e:
        return {"error": e.detail}

# 3. 查询报销单状态
@app.get("/get_bill/{bill_id}")
def get_bill(bill_id: str):
    if bill_id not in bill_database:
        raise HTTPException(status_code=404, detail="报销单不存在")
    return bill_database[bill_id]

# ====================== 测试入口（命令行交互） ======================
if __name__ == "__main__":
    # 启动 FastAPI 服务（本地访问：http://127.0.0.1:8000/docs 可测试接口）
    print("智能报销审批 Demo 启动中...")
    print("访问 http://127.0.0.1:8000/docs 可打开 Swagger 测试界面")
    
    # 改用Uvicorn底层API启动，适配已有事件循环的环境
    config = Config(
        app=app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
    server = Server(config=config)
    # 启动服务（自动适配已有事件循环）
    server.run()
