import re

from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True

        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href":text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
    else:
        raise Exception("Invalid text node type")
    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text)%2 == 0:
                raise Exception("Invalid Markdown syntax")
            else:
                for i in range(len(split_text)):
                    if split_text[i] == "":
                        continue
                    if i%2 == 0:
                        new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(split_text[i], text_type))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            text = node.text
            image_matches = extract_markdown_images(node.text)
            if len(image_matches) == 0:
                new_nodes.append(node)
                continue
            split_text = []
            for image in image_matches:
                image_text = f"![{image[0]}]({image[1]})"
                split_text_temp = text.split(image_text, 1)
                if len(split_text_temp) != 2:
                    raise Exception("Invalid Image markdown")
                split_text.append(split_text_temp[0])
                split_text.append(image)
                text = split_text_temp[-1]
            split_text.append(text)
            for i in range(len(split_text)):
                if split_text[i] == "":
                    continue
                if i%2 == 0:
                    new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_text[i][0], TextType.IMAGE, split_text[i][1]))
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            text = node.text
            link_matches = extract_markdown_links(node.text)
            if len(link_matches) == 0:
                new_nodes.append(node)
                continue
            split_text = []
            for link in link_matches:
                link_text = f"[{link[0]}]({link[1]})"
                split_text_temp = text.split(link_text, 1)
                if len(split_text_temp) != 2:
                    raise Exception("Invalid Link markdown")
                split_text.append(split_text_temp[0])
                split_text.append(link)
                text = split_text_temp[-1]
            split_text.append(text)
            for i in range(len(split_text)):
                if split_text[i] == "":
                    continue
                if i%2 == 0:
                    new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_text[i][0], TextType.LINK, split_text[i][1]))

    return new_nodes

def text_to_textnodes(text):
    text_node = [TextNode(text, TextType.TEXT)]
    text_node = split_nodes_delimiter(text_node, "**", TextType.BOLD)
    text_node = split_nodes_delimiter(text_node, "_", TextType.ITALIC)
    text_node = split_nodes_delimiter(text_node, "`", TextType.CODE)
    text_node = split_nodes_images(text_node)
    text_node = split_nodes_links(text_node)
    return text_node


