import shutil
import os
import sys

from textnode import TextNode, text_to_textnodes, text_node_to_html_node, TextType
from blocknode import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import HTMLNode, ParentNode

basepath = sys.argv[1] if 1 < len(sys.argv) else "/"

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))

    return children


    
def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    div_children = []
    for block in md_blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.CODE:
            text_node = TextNode("\n".join(block.split("\n")[1:-1]), TextType.TEXT)
            children = [text_node_to_html_node(text_node)]
            html_node = ParentNode("code", children)
            html_node_code = ParentNode("pre", [html_node])
            div_children.append(html_node_code)
        elif block_type == BlockType.HEADING:
            block_split = block.split(" ", 1)
            children = text_to_children(block_split[1])
            html_node = ParentNode(f"h{len(block_split[0])}", children)
            div_children.append(html_node)
        elif block_type == BlockType.ORDERED_LIST:
            children = []
            block_split = block.split("\n")
            for line in block_split:
                line_split = line.split(" ", 1)
                children.append(ParentNode("li", text_to_children(line_split[1])))
            html_node = ParentNode("ol", children)
            div_children.append(html_node)
        elif block_type == BlockType.UNORDERED_LIST:
            children = []
            block_split = block.split("\n")
            for line in block_split:
                line_split = line.split(" ", 1)
                children.append(ParentNode("li", text_to_children(line_split[1])))
            html_node = ParentNode("ul", children)
            div_children.append(html_node)
        elif block_type == BlockType.QUOTE:
            children = []
            block_split = block.split("\n")
            for line in block_split:
                children.extend(text_to_children(line[1:].strip()))
            html_node = ParentNode("blockquote", children)
            div_children.append(html_node)
        else:
            children = text_to_children(block.replace("\n", " "))
            html_node = ParentNode("p", children)
            div_children.append(html_node)
        
    return ParentNode("div", div_children)


def copy_directory(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    

    shutil.copytree(src, dst)

def extract_title(markdown):
    return markdown.split("# ")[1].split("\n")[0]

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    source_file_content = ""
    with open(from_path) as f:
        source_file_content = f.read()
    dest_file_content = ""
    with open(template_path) as f:
        dest_file_content = f.read()
    html = markdown_to_html_node(source_file_content).to_html()
    title = extract_title(source_file_content)
    dest_file_content = dest_file_content.replace("{{ Content }}", html)
    dest_file_content = dest_file_content.replace("{{ Title }}", title)
    dest_file_content = dest_file_content.replace('href="/', f'href="{basepath}')
    dest_file_content = dest_file_content.replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(dest_file_content)

def generate_pages_recursive(source_path, dest_path, template_path):
    for root, dirs, files in os.walk(source_path):
        rel_path = os.path.relpath(root, source_path)
        dest_dir = os.path.join(dest_path, rel_path)

        os.makedirs(dest_dir, exist_ok=True)

        for file in files:
            if file.endswith("md"):
                src_file = os.path.join(root, file)
                html_filename = file.replace(".md", ".html")
                dest_file = os.path.join(dest_dir, html_filename)

                generate_page(src_file, template_path, dest_file)



def main():
    copy_directory("/Users/ayushverma/workspace/bootdotdev/static-site/static", "/Users/ayushverma/workspace/bootdotdev/static-site/docs")
    generate_pages_recursive("/Users/ayushverma/workspace/bootdotdev/static-site/content", "/Users/ayushverma/workspace/bootdotdev/static-site/docs", "/Users/ayushverma/workspace/bootdotdev/static-site/template.html")

main()
