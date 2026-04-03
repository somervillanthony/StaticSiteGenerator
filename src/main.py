import os
import shutil
import sys
from inline_markdown import markdown_to_html_node

def main():
     if len(sys.argv) > 1:
          basepath = sys.argv[1]
     else:
          basepath = ""
     source = os.path.join(basepath, "static")
     dest = os.path.join(basepath, "docs")
     public_creator(source, dest)
     content = os.path.join(basepath, "content")
     generate_pages_recursive(content, "template.html", dest, basepath)


def public_creator(source, destination):
     copy_log = []
     if not os.path.exists(source):
          raise Exception("Not a valid source")
     if os.path.exists(destination):
          shutil.rmtree(destination)
          os.mkdir(destination)
     else:
          os.mkdir(destination)
     def content_copier(source, destination):
          source_list = os.listdir(source)
          for item in source_list:
               item_path = os.path.join(source, item)
               if os.path.isfile(item_path):
                    shutil.copy(item_path, destination)
                    copy_log.append(f"{item}:{destination}")
               else:
                    dir_path = os.path.join(destination, item)
                    os.mkdir(dir_path)
                    content_copier(item_path, dir_path)
     return content_copier(source, destination)
                  
def extract_title(markdown):
     stripped_markdown = markdown.strip()
     if stripped_markdown.startswith("# "):
          heading_string = stripped_markdown[2:]
          return heading_string
     raise Exception("improper markdown syntax for a h1 heading")

def generate_page(from_path, template_path, dest_path, basepath):
     print(f"Generating page from {from_path} to {dest_path} using {template_path}")
     markdown = open(from_path, "r").read()
     template = open(template_path, "r").read()

     node = markdown_to_html_node(markdown)
     html_string = node.to_html()

     markdown_lines = markdown.split("\n")
     title = extract_title(markdown_lines[0])

     html_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
     html_page = html_page.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
     directories = os.path.dirname(dest_path)
     os.makedirs(directories, exist_ok=True)
     f = open(dest_path, "w")
     f.write(html_page)
     f.close()
  
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
     dir_list = os.listdir(dir_path_content)
     for item in dir_list:
          item_path = os.path.join(dir_path_content, item)
          if not os.path.isfile(item_path):
               new_dest_path = os.path.join(dest_dir_path, item)
               generate_pages_recursive(item_path, template_path, new_dest_path, basepath)
          elif item == "index.md":
               new_dest_path = os.path.join(dest_dir_path, "index.html")
               generate_page(item_path, template_path, new_dest_path, basepath)

main()
