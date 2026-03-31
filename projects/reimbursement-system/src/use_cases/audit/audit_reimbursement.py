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
