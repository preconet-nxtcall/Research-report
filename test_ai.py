import asyncio
import os

from backend.services.ai_service import generate_research_report

async def main():
    if not os.getenv("OPENAI_API_KEY"):
        from dotenv import load_dotenv
        env_path = os.path.join(os.path.dirname(__file__), "backend", ".env")
        load_dotenv(env_path)
    
    try:
        report = await generate_research_report("Reliance Industries")
        print(report.model_dump_json(indent=2))
    except Exception as e:
        print("Error:")
        print(e)

if __name__ == "__main__":
    asyncio.run(main())
