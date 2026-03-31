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
