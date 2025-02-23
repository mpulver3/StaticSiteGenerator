import os
import shutil
from textnode import *
from htmlnode import *
from markdown_blocks import *

'''def main(text, text_type, url):
    node = TextNode(text, text_type, url)
    htmlnode = HTMLNode("a", "text", {"href": "https://www.google.com","target": "_blank"})
    print(node)
    print(htmlnode)
    print(htmlnode.props_to_html())

main("This is a text node", TextType.BOLD, "https://www.boot.dev")'''

def main():
    copy_contents()
    generate_page("/home/xunil/workspace/github.com/mpulver3/StaticSiteGen/content/index.md", "/home/xunil/workspace/github.com/mpulver3/StaticSiteGen/template.html", "/home/xunil/workspace/github.com/mpulver3/StaticSiteGen/public/index.html")
    return

#copies the contents from the source directory to the destination directory
#statically use sStaticSiteGen/static and StaticSiteGen/public respectively
#Should clean the destination directory
#Copy all files and subdirectories
#log the path of each file that is copied
def copy_contents(source_path='/home/xunil/workspace/github.com/mpulver3/StaticSiteGen/static', dest_path='/home/xunil/workspace/github.com/mpulver3/StaticSiteGen/public'):
    list_contents = os.listdir(path=source_path)
    if os.path.exists(path=dest_path):
        shutil.rmtree(path=dest_path, ignore_errors=True, onerror=None)
    os.mkdir(path=dest_path)
    for item in list_contents:
        full_source_item = source_path + "/" + item
        if os.path.isfile(full_source_item):
            shutil.copy(full_source_item, dest_path)
            print(f"Copying {full_source_item} to {dest_path}")
        else:
            full_dest_folder = dest_path + "/" + item
            copy_contents(full_source_item, full_dest_folder)
    return



def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as from_contents:
        markdown_contents = from_contents.read()
    with open(template_path, "r") as temp_contents:
        template_contents = temp_contents.read()
    html_contents = markdown_to_html_node(markdown_contents)
    html_contents = html_contents.to_html()
    title = extract_title(markdown_contents)
    title_split = template_contents.split("{{ Title }}")
    content_split = title_split[1].split("{{ Content }}")
    html_page = title_split[0] + title + content_split[0] + html_contents + content_split[1]
    with open(dest_path, "a") as new_file:
        new_file.write(html_page)


main()