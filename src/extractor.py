import re

def extract_markdown_images(text: str):
    return re.findall(r"!\[([^\]]*)\]\(([^)]*)\)", text)

def extract_markdown_links(text: str):
    return re.findall(r"(?<!!)\[([^\]]*)\]\(([^)]*)\)", text)

def extract_header(text: str):
    pattern = re.compile(r"^#{1,6}\s.*")
    return re.findall(pattern, text)

def extract_title(text: str):
    pattern = re.compile(r"^#{1}\s.*")
    capture = re.findall(pattern, text) 
    try:
        title = str.strip(capture[0][1:])
    except:
        raise ValueError("Title not found, e.g. # i am title")
    return title

def extract_multiline_code(text: str):
    pattern = re.compile(r"^```\n.*```")
    return re.findall(pattern, text)

