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
    **kwargs,
):
    if kwargs.get("verbose", True):
        print(f"Start: {datetime.datetime.now()} for file {src}")
    with open(src, "r") as f:
        content = f.read()

    document = doctran.parse(content=content)
    transformed = document.translate(language="japanese").execute().transformed_content

    with open(dst, "w") as f:
        f.write(transformed)

    if kwargs.get("verbose", True):
        print(f"End: {datetime.datetime.now()} for file {src}")

    return


def walk(dir: str = "fixtures", **kwargs):
    """Walk through all *.md files in the directory

    :param bool skip_ja: skip files with .ja.md extension
    :param bool skip_translated: if *.ja.md exists, skip *.md
    """
    srcs, dsts = [], []
    files = list(pathlib.Path(dir).glob("**/*.md"))
    for file in files:
        src = file
        if kwargs.get("skip_ja", False) and ".ja.md" in str(src):
            continue

        dst = file.with_suffix(".ja.md")
        if kwargs.get("skip_translated", False) and dst.exists():
            continue

        srcs.append(src)
        dsts.append(dst)

    return srcs, dsts


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, default="fixtures")
    parser.add_argument("--throttle", type=int, default=10)
    parser.add_argument("--key", type=str, default=OPENAI_API_KEY)
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--skip", action="store_true")
    parser.add_argument("--dry", "-d", action="store_true")
    args = parser.parse_args()

    _executor = ThreadPoolExecutor(args.throttle)
    loop = asyncio.get_event_loop()

    async def translate_file_async(src, dst):
        await loop.run_in_executor(_executor, translate_file, src, dst)

    files = walk(
        dir=args.dir,
        skip_ja=args.skip,
        sip_translated=args.skip,
    )

    if args.verbose:
        for src, dst in zip(*files):
            print(src)
            print(dst)

    if args.verbose:
        print(args)

    if not args.dry:
        tasks = [translate_file_async(src, dst) for src, dst in zip(*files)]
        loop.run_until_complete(asyncio.gather(*tasks))
