from generator import generate_pages_recursive
from copier import copy_src_to_dest
import os
import shutil

def main():

    public_dir = "public"
    static_dir = "static"

    if os.path.exists(public_dir):
        print(f"DELETE DIR: {public_dir}")
        shutil.rmtree(public_dir)

    copy_src_to_dest(static_dir, public_dir)

    generate_pages_recursive("content", "template.html", "public")

main()
