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
