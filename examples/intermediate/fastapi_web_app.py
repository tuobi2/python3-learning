#!/usr/bin/env python3
"""
FastAPI Web应用示例 - 智能报销审批系统

一个完整的FastAPI Web应用示例，展示：
1. FastAPI基础使用
2. Pydantic数据验证
3. RESTful API设计
4. 错误处理
5. 异步支持
6. API文档自动生成
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum
import random
import uvicorn


# ====================== 数据模型定义 ======================

class ExpenseType(str, Enum):
    """费用类型枚举"""
    TRAVEL = "差旅费"
    MEAL = "餐饮费"
    OFFICE = "办公费"
    TRAINING = "培训费"
    TRANSPORT = "交通费"
    OTHER = "其他费用"


class ReimbursementStatus(str, Enum):
    """报销状态枚举"""
    DRAFT = "草稿"
    PENDING_REVIEW = "待初审"
    PENDING_APPROVAL = "待审批"
    APPROVED = "已通过"
    REJECTED = "已驳回"
    ARCHIVED = "已归档"


class ReimbursementBill(BaseModel):
    """报销单数据模型"""
    employee_name: str = Field(..., min_length=2, max_length=50, description="员工姓名")
    employee_dept: str = Field(..., min_length=2, max_length=50, description="所属部门")
    amount: float = Field(..., gt=0, le=100000, description="报销金额（0-100,000）")
    expense_type: Optional[ExpenseType] = Field(None, description="费用类型")
    invoice_num: str = Field(..., min_length=8, max_length=50, description="发票号码")
    invoice_date: str = Field(..., description="发票日期")
    reason: str = Field(..., min_length=5, max_length=500, description="报销事由")
    status: ReimbursementStatus = Field(default=ReimbursementStatus.DRAFT, description="报销状态")
    reject_reason: Optional[str] = Field(None, description="驳回原因")
    approval_user: Optional[str] = Field(None, description="审批人")
    create_time: Optional[str] = Field(None, description="创建时间")
    bill_id: Optional[str] = Field(None, description="报销单ID")
    
    @validator('invoice_date')
    def validate_invoice_date(cls, v):
        """验证发票日期格式"""
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("发票日期格式应为 YYYY-MM-DD")
    
    @validator('amount')
    def validate_amount(cls, v):
        """验证金额格式"""
        if v <= 0:
            raise ValueError("报销金额必须大于0")
        # 保留两位小数
        return round(v, 2)


class ApprovalRequest(BaseModel):
    """审批请求模型"""
    approve: bool = Field(True, description="是否批准")
    approver_name: str = Field(..., min_length=2, max_length=50, description="审批人姓名")
    comment: Optional[str] = Field(None, max_length=500, description="审批意见")


class DepartmentBudget(BaseModel):
    """部门预算模型"""
    department: str
    total_budget: float
    used_budget: float = 0.0
    
    @property
    def remaining_budget(self) -> float:
        """剩余预算"""
        return self.total_budget - self.used_budget


# ====================== 应用初始化 ======================

app = FastAPI(
    title="智能报销审批系统",
    description="基于FastAPI的智能报销审批系统示例",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# ====================== 模拟数据存储 ======================

# 报销单数据库
bill_database: Dict[str, ReimbursementBill] = {}

# 部门预算数据
department_budgets: Dict[str, DepartmentBudget] = {
    "技术部": DepartmentBudget(department="技术部", total_budget=10000),
    "财务部": DepartmentBudget(department="财务部", total_budget=8000),
    "市场部": DepartmentBudget(department="市场部", total_budget=15000),
    "人事部": DepartmentBudget(department="人事部", total_budget=5000),
}

# 费用类型匹配规则
expense_type_rules: Dict[str, ExpenseType] = {
    "打车": ExpenseType.TRANSPORT,
    "机票": ExpenseType.TRAVEL,
    "酒店": ExpenseType.TRAVEL,
    "餐饮": ExpenseType.MEAL,
    "办公用品": ExpenseType.OFFICE,
    "培训": ExpenseType.TRAINING,
    "快递": ExpenseType.OFFICE,
}

# 审批规则
approval_rules = {
    "low": {"max_amount": 500, "approver": "部门经理"},
    "mid": {"max_amount": 3000, "approver": "财务主管"},
    "high": {"max_amount": float("inf"), "approver": "总经理"},
}


# ====================== 核心业务逻辑 ======================

def generate_bill_id() -> str:
    """生成报销单ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_num = random.randint(1000, 9999)
    return f"BILL-{timestamp}-{random_num}"


def detect_expense_type(reason: str) -> ExpenseType:
    """根据事由检测费用类型"""
    reason_lower = reason.lower()
    for keyword, expense_type in expense_type_rules.items():
        if keyword in reason_lower:
            return expense_type
    return ExpenseType.OTHER


def ai_fill_bill(bill: ReimbursementBill) -> ReimbursementBill:
    """AI智能填单"""
    # 生成ID
    bill.bill_id = generate_bill_id()
    
    # 检测费用类型
    if not bill.expense_type:
        bill.expense_type = detect_expense_type(bill.reason)
    
    # 设置创建时间
    bill.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 更新状态
    bill.status = ReimbursementStatus.PENDING_REVIEW
    
    return bill


def ai_review_bill(bill: ReimbursementBill) -> ReimbursementBill:
    """AI智能初审"""
    reject_reasons = []
    
    # 1. 校验发票号格式
    if not bill.invoice_num.replace("-", "").isalnum():
        reject_reasons.append("发票号格式错误，应包含字母和数字")
    
    # 2. 校验部门预算
    if bill.employee_dept not in department_budgets:
        reject_reasons.append(f"部门'{bill.employee_dept}'不存在")
    else:
        budget = department_budgets[bill.employee_dept]
        if bill.amount > budget.remaining_budget:
            reject_reasons.append(
                f"部门预算不足（剩余预算：{budget.remaining_budget:.2f}元）"
            )
    
    # 3. 校验金额合理性
    if bill.amount > 10000 and bill.expense_type == ExpenseType.MEAL:
        reject_reasons.append("餐饮费单笔不能超过10,000元")
    
    # 根据校验结果更新状态
    if reject_reasons:
        bill.status = ReimbursementStatus.REJECTED
        bill.reject_reason = "; ".join(reject_reasons)
    else:
        bill.status = ReimbursementStatus.PENDING_APPROVAL
        # 自动匹配审批人
        if bill.amount <= approval_rules["low"]["max_amount"]:
            bill.approval_user = approval_rules["low"]["approver"]
        elif bill.amount <= approval_rules["mid"]["max_amount"]:
            bill.approval_user = approval_rules["mid"]["approver"]
        else:
            bill.approval_user = approval_rules["high"]["approver"]
        
        # 更新部门预算
        department_budgets[bill.employee_dept].used_budget += bill.amount
    
    return bill


def manual_approve_bill(bill_id: str, request: ApprovalRequest) -> ReimbursementBill:
    """人工审批报销单"""
    if bill_id not in bill_database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="报销单不存在"
        )
    
    bill = bill_database[bill_id]
    
    if bill.status != ReimbursementStatus.PENDING_APPROVAL:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="当前报销单不处于待审批状态"
        )
    
    if request.approve:
        bill.status = ReimbursementStatus.APPROVED
        # 审批通过后自动归档
        bill.status = ReimbursementStatus.ARCHIVED
        if request.comment:
            bill.reject_reason = f"审批意见: {request.comment}"
    else:
        bill.status = ReimbursementStatus.REJECTED
        bill.reject_reason = request.comment or "人工审批驳回"
        # 退回预算
        department_budgets[bill.employee_dept].used_budget -= bill.amount
    
    return bill


# ====================== API接口定义 ======================

@app.get("/")
async def root():
    """根路径，返回欢迎信息"""
    return {
        "message": "欢迎使用智能报销审批系统",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database_size": len(bill_database)
    }


@app.post("/bills", response_model=ReimbursementBill, status_code=status.HTTP_201_CREATED)
async def submit_bill(bill: ReimbursementBill):
    """
    提交报销单
    
    - **AI自动填单**: 生成ID、检测费用类型、记录时间
    - **AI智能初审**: 校验发票、预算、金额合理性
    - **自动匹配审批人**: 根据金额匹配相应审批人
    """
    # AI智能填单
    filled_bill = ai_fill_bill(bill)
    
    # AI智能初审
    reviewed_bill = ai_review_bill(filled_bill)
    
    # 存入数据库
    bill_database[filled_bill.bill_id] = reviewed_bill
    
    return reviewed_bill


@app.get("/bills", response_model=List[ReimbursementBill])
async def list_bills(
    status: Optional[ReimbursementStatus] = None,
    department: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """
    查询报销单列表
    
    支持按状态、部门筛选，支持分页
    """
    bills = list(bill_database.values())
    
    # 筛选
    if status:
        bills = [b for b in bills if b.status == status]
    if department:
        bills = [b for b in bills if b.employee_dept == department]
    
    # 分页
    return bills[skip:skip + limit]


@app.get("/bills/{bill_id}", response_model=ReimbursementBill)
async def get_bill(bill_id: str):
    """根据ID查询报销单"""
    if bill_id not in bill_database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="报销单不存在"
        )
    return bill_database[bill_id]


@app.post("/bills/{bill_id}/approve", response_model=ReimbursementBill)
async def approve_bill(bill_id: str, request: ApprovalRequest):
    """审批报销单"""
    return manual_approve_bill(bill_id, request)


@app.get("/departments/budget")
async def get_department_budgets():
    """获取所有部门预算信息"""
    return [
        {
            "department": budget.department,
            "total_budget": budget.total_budget,
            "used_budget": budget.used_budget,
            "remaining_budget": budget.remaining_budget,
            "usage_rate": f"{(budget.used_budget / budget.total_budget * 100):.1f}%"
        }
        for budget in department_budgets.values()
    ]


@app.get("/statistics")
async def get_statistics():
    """获取统计信息"""
    total_bills = len(bill_database)
    total_amount = sum(b.amount for b in bill_database.values())
    
    # 按状态统计
    status_count = {}
    for bill in bill_database.values():
        status_count[bill.status] = status_count.get(bill.status, 0) + 1
    
    # 按部门统计
    dept_count = {}
    dept_amount = {}
    for bill in bill_database.values():
        dept_count[bill.employee_dept] = dept_count.get(bill.employee_dept, 0) + 1
        dept_amount[bill.employee_dept] = dept_amount.get(bill.employee_dept, 0) + bill.amount
    
    return {
        "total_bills": total_bills,
        "total_amount": total_amount,
        "average_amount": total_amount / total_bills if total_bills > 0 else 0,
        "status_distribution": status_count,
        "department_distribution": {
            "count": dept_count,
            "amount": dept_amount
        },
        "timestamp": datetime.now().isoformat()
    }


# ====================== 错误处理 ======================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP异常处理"""
    return {
        "error": {
            "code": exc.status_code,
            "message": exc.detail,
            "path": request.url.path
        }
    }


# ====================== 启动函数 ======================

def print_welcome_message():
    """打印欢迎信息"""
    print("=" * 70)
    print("智能报销审批系统 (FastAPI版)")
    print("=" * 70)
    print("架构特点:")
    print("  • 基于FastAPI的现代Web框架")
    print("  • 使用Pydantic进行数据验证")
    print("  • RESTful API设计")
    print("  • 自动生成API文档")
    print("  • 异步支持")
    print()
    print("访问地址:")
    print("  • API文档: http://127.0.0.1:8000/docs")
    print("  • ReDoc文档: http://127.0.0.1:8000/redoc")
    print("  • 健康检查: http://127.0.0.1:8000/health")
    print("=" * 70)


if __name__ == "__main__":
    print_welcome_message()
    
    # 启动FastAPI服务
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=False
    )