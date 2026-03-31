import os
import shutil

def copy_src_to_dest(src, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)
    child_list = os.listdir(src)

    if len(child_list) == 0:
        return

    for child in child_list:
        src_path = os.path.join(src, child)
        dest_path = os.path.join(dest, child)

        if not os.path.isfile(src_path):
            print(f"MKDIR: {src_path} {dest_path}")

            if not os.path.exists(dest_path):
                os.mkdir(dest_path)

            copy_src_to_dest(src_path, dest_path)

        else:
            print(f"COPY: {src_path} {dest_path}")
            shutil.copy(src_path, dest_path)

# copy_src_to_dest("static", "public")

