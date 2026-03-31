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
