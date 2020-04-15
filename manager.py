import os, json, re, requests
from pathlib import Path

GITHUB_MODULES = ['command-line', 'data', 'databases', 'ethics', 'geospatialdata', 'git', 'glossary', 'guide', 'html-css', 'install', 'jekyll', 'machine-learning', 'mapping', 'omeka', 'project-lab', 'python', 'r', 'text-analysis', 'twitter-api', 'website-template']
GITHUB_LINKS = github_links = [f"https://github.com/DHRI-Curriculum/{x}.git" for x in GITHUB_MODULES]
SUBDIRECTORY = './github-curricula'

def _clone_all_github():
  for link in GITHUB_LINKS:
    module = link.split("/")[-1][:-4]
    if Path(f"{SUBDIRECTORY}/{module}").exists():
        print(f"\n{module} has already been downloaded.")
    else:
        os.system(f"git clone {link} {SUBDIRECTORY}/{module}")

def _copy(self, target):
    import shutil
    assert self.is_file()
    shutil.copy(str(self), str(target))  # str() only there for Python < (3, 6)

def find_files(filename, search_path):
  __ = []
  for root, _, files in os.walk(search_path):
    if filename in files:
      __.append(os.path.join(root, filename))
  return __

def load_order():
  return(json.loads(Path("order.json").read_text()))

def write_notebook(name, cells):
    data = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
            "display_name": "'Python Interactive'",
            "language": "python",
            "name": "a6fb91d6-314b-425d-9177-d51c94f82bf0"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    Path(f'./notebooks/{name}.ipynb').write_text(json.dumps(data))

def get_file(_from, to):
  q = requests.get(_from)
  if not to.parent.exists(): to.parent.mkdir(parents=True)
  to.write_bytes(q.content)