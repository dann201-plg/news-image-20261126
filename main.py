"""Entry point for the 26 November 2026 news image (news-image-20261126).

Runs the generator, which writes entry.png next to this file, then copies
it to the output directory so the grader can find it.
"""

import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    subprocess.run([sys.executable, os.path.join(HERE, "draw_news26.py")],
                   check=True)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
