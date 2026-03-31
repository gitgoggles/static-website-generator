from pathlib import Path
import os
from conversion import *


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as m, open(template_path) as t:
        md_file = m.read()
        template_file = t.read()

        title = extract_title(md_file)
        html_node = markdown_to_html_node(md_file)
        html = html_node.to_html()

        page = template_file
        page = page.replace("{{ Title }}", title)
        page = page.replace("{{ Content }}", html)
        page = page.replace('href="/', f'href="{basepath}')
        page = page.replace('src="/', f'src="{basepath}')

        dest_path = Path(dest_path)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, "w") as new_file:
            new_file.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    file_list = os.listdir(dir_path_content)
    for file in file_list:
        src_file_path = os.path.join(dir_path_content, file)
        dest_file_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(src_file_path):
            generate_page(src_file_path, template_path, Path(dest_file_path).with_suffix(".html"), basepath)
        else:
            generate_pages_recursive(src_file_path, template_path, dest_file_path, basepath)



