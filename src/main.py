from generator import generate_pages_recursive
from copier import copy_src_to_dest
import os
import shutil
import sys

def main():

    public_dir = "docs"
    static_dir = "static"
    basepath = "/"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    if os.path.exists(public_dir):
        print(f"DELETE DIR: {public_dir}")
        shutil.rmtree(public_dir)

    copy_src_to_dest(static_dir, public_dir)

    generate_pages_recursive("content", "template.html", public_dir, basepath)

main()
