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
