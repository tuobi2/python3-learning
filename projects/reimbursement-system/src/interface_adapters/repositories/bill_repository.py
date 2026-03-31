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
