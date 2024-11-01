from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
<<<<<<< HEAD
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
=======
    image_markdown_matches = re.findall("(!\[.*?\])(\(.*?\))", text)
    images = []
    for match in image_markdown_matches:
        alt_text = match[0][2 : len(match[0]) - 1]
        image_url = match[1][1 : len(match[1]) - 1]
        images.append((alt_text, image_url))
    return images


def extract_markdown_links(text):
    link_markdown_matches = re.findall("([^!]\[.*?\])(\(.*?\))", text)
    links = []
    for link in link_markdown_matches:
        link_text = link[0][2 : len(link[0]) - 1]
        link_url = link[1][1 : len(link[1]) - 1]
        links.append((link_text, link_url))
    return links
>>>>>>> 9e2f3586fcc3b76b28eaad7ab63602bdad671fb6
