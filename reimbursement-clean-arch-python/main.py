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
