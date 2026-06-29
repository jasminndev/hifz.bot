import asyncio
from db.session import create_tables


async def main():
    await create_tables()
    print("✅ Tables created successfully!")


asyncio.run(main())
