reimbursement_clean_arch/
├── src/
│   ├── domain/                  # 1. Entities 实体层
│   │   ├── entities/
│   │   │   ├── bill.py          # 报销单实体
│   │   │   └── notification.py  # 通知实体
│   │   └── value_objects/       # 值对象（不可变）
│   │       ├── amount.py
│   │       └── expense_type.py
│   ├── use_cases/               # 2. Use Cases 用例层（智能体核心逻辑）
│   │   ├── classify/
│   │   │   └── classify_expense.py
│   │   ├── audit/
│   │   │   └── audit_reimbursement.py
│   │   ├── finance/
│   │   │   └── generate_bill.py
│   │   ├── notify/
│   │   │   └── send_notification.py
│   │   └── dispatcher/
│   │       └── process_reimbursement.py
│   ├── interface_adapters/      # 3. Interface Adapters 接口适配层
│   │   ├── repositories/        # 数据库适配
│   │   │   ├── bill_repository.py
│   │   │   └── notification_repository.py
│   │   ├── llm/                 # LLM适配
│   │   │   └── spark_llm_adapter.py
│   │   └── invoice/             # 发票工具适配
│   │       └── invoice_adapter.py
│   └── frameworks/              # 4. Frameworks & Drivers 框架驱动层
│       ├── api/
│       │   └── fastapi_app.py
│       └── config/
│           └── settings.py
└── main.py                      # 启动入口
