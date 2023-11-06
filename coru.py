import asyncio
import time
from concurrent.futures import ThreadPoolExecutor


_executor = ThreadPoolExecutor(3)


def sync_blocking():
    print("before sync_blocking")
    time.sleep(1)
    print("after sync_blocking")


async def hello_world():
    # run blocking function in another thread,
    # and wait for it's result:
    await loop.run_in_executor(_executor, sync_blocking)


loop = asyncio.get_event_loop()
tasks = asyncio.gather(*[hello_world() for _ in range(10)])
loop.run_until_complete(tasks)
loop.close()
