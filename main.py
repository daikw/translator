#!/usr/bin/env python

import os
import argparse
import asyncio
import datetime
import pathlib
from concurrent.futures import ThreadPoolExecutor

from doctran import Doctran

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

doctran = Doctran(openai_api_key=OPENAI_API_KEY)


def translate_file(
    src: str = "fixtures/test_en.md",
    dst: str = "fixtures/test_ja.md",
):
    if verbose:
        print(f"Start: {datetime.datetime.now()} for file {src}")
    with open(src, "r") as f:
        content = f.read()

    document = doctran.parse(content=content)
    transformed = document.translate(language="japanese").execute().transformed_content

    with open(dst, "w") as f:
        f.write(transformed)

    if verbose:
        print(f"End: {datetime.datetime.now()} for file {src}")

    return


# walk through all files in the directory, except for the ones like *.ja.md
def walk(dir: str = "fixtures"):
    srcs, dsts = [], []
    for file in pathlib.Path(dir).glob("**/*.md"):
        src = file
        if ".ja.md" in str(file):
            continue

        dst = file.with_suffix(".ja.md")
        srcs.append(src)
        dsts.append(dst)
        if verbose:
            print(src)
            print(dst)

    return zip(srcs, dsts)


verbose = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, default="fixtures")
    parser.add_argument("--throttle", type=int, default=10)
    parser.add_argument("--key", type=str, default=OPENAI_API_KEY)
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    verbose = args.verbose

    _executor = ThreadPoolExecutor(args.throttle)
    loop = asyncio.get_event_loop()

    async def translate_file_async(src, dst):
        await loop.run_in_executor(_executor, translate_file, src, dst)

    tasks = [translate_file_async(src, dst) for src, dst in walk(dir=args.dir)]
    loop.run_until_complete(asyncio.gather(*tasks))
