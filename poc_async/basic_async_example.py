import asyncio

async def task(name, seconds):
    print(f"starting task {name}")
    await asyncio.sleep(seconds) # non-blocking sleep
    print(f"finished task {name}")

async def main():
    await asyncio.gather(
        task("A", 2),
        task("B", 2)
    )

if __name__ == "__main__":
    asyncio.run(main())