from manager import load_order, write_notebook, _clone_all_github, find_files, _copy, Path, get_file
import re

Path.copy = _copy

IMG_REGEX = re.compile(r"(?:!\[(.*?)\]\((.*?)\))")



order = load_order()
_clone_all_github()



search_file = False
in_cell, in_code = False, False


for module in Path("./github-curricula").glob("*"):
    try:
        sections = order['order'][module.stem]
    except KeyError:
        continue

    cells = []
    for section in sections:
        file_name = Path('./github-curricula') / module.stem / 'sections' / (section + ".md")
        md = file_name.read_text()
        lines = md.split("\n")
        for i, line in enumerate(lines):
            if len(line):
                if "<<<" in line: continue # skipping nav lines

                is_header = line.strip().startswith("#")
                is_code = line.strip().startswith("```")
                is_image = re.search(IMG_REGEX, line)

                if is_image and in_cell:
                    alt_text = is_image.groups()[0].replace('"', "'") # fixing up nested quotation marks so they don't cause trouble in html
                    link = is_image.groups()[1]
                    if not link.startswith("."):
                        if re.search(r"(https?:\/\/)?(www.)?github.com\/", link):
                            # link is on github - easy!
                            raw_link = "https://raw.githubusercontent.com/" + re.sub(r"(https?:\/\/)?(www.)?github.com\/", "", link).replace("/blob", "")
                            file_name = raw_link.split("/")[-1]
                            local_path = Path(f"./notebooks/img/{module.stem}/{file_name}")
                            if not local_path.exists():
                                get_file(raw_link, local_path)

                            new_link = f"./img/{module}/{file_name}"
                            this_cell['source'].extend([f"![{alt_text}]({new_link})"])
                            continue
                        else:
                            search_file = True
                    else:
                        search_file = True

                if search_file:
                    found = find_files(Path(link).name,"./github-curricula/")
                    if len(found):
                        print(f"Warning: found local images that matches the one found in module {module.stem} ({link}): could be wrong image but including it in the resulting notebook.")
                        found_file = Path(found[0])
                        new_file = Path(f"./notebooks/img/{module.stem}/{found_file.name}")
                        if not new_file.parent.exists(): new_file.parent.mkdir(parents=True)
                        Path(found_file).copy(new_file)
                        print(f"Copying {found_file} --> {new_file}")
                        new_link = Path(f"./img/{module.stem}/{found_file.name}")
                        this_cell['source'].extend([f"![{alt_text}]({new_link})"])
                        search_file = False
                        continue
                    else:
                        print("No files could be found")
                        search_file = False


                if is_code and in_cell:
                    if "python" in line.lower() and not in_code:
                        try:
                            if this_cell['source'][-1] == "\n":
                                this_cell['source'].pop()
                            this_cell['source'].append(this_cell['source'].pop().replace("\n", ""))
                            cells.append(this_cell)
                        except NameError:
                            pass
                        except IndexError:
                            pass
                        this_cell = {"cell_type": "code", "metadata": {}, "outputs": [], "execution_count": None, "source": []}
                        in_code = True
                        continue
                    elif line.strip() == "```" and in_code:
                        try:
                            if this_cell['source'][-1] == "\n":
                                this_cell['source'].pop()
                            this_cell['source'].append(this_cell['source'].pop().replace("\n", ""))
                            cells.append(this_cell)
                        except NameError:
                            pass
                        except IndexError:
                            pass
                        this_cell = {"cell_type": "markdown", "metadata": {}, "source": []}
                        in_code = False
                        continue
                if in_code:
                    line = line.replace("\t", "    ")
                    this_cell['source'].extend([line + "\n"])
                    continue


                if is_header and not in_cell:
                    in_cell = True
                    try:
                        if this_cell['source'][-1] == "\n":
                            this_cell['source'].pop()
                        this_cell['source'].append(this_cell['source'].pop().replace("\n", ""))
                        cells.append(this_cell)
                    except NameError:
                        pass
                    except IndexError:
                        pass
                    this_cell = {"cell_type": "markdown", "metadata": {}, "source": []}
                    this_cell['source'].extend([line + "\n", "\n"])
                    continue
                elif is_header and in_cell:
                    # end cell, start new
                    in_cell = True
                    try:
                        if this_cell['source'][-1] == "\n":
                            this_cell['source'].pop()
                        this_cell['source'].append(this_cell['source'].pop().replace("\n", ""))
                        cells.append(this_cell)
                    except NameError:
                        pass
                    except IndexError:
                        pass
                    this_cell = {"cell_type": "markdown", "metadata": {}, "source": []}
                    this_cell['source'].extend([line + "\n", "\n"])
                    continue
                elif not is_header and in_cell:
                    this_cell['source'].extend([line + "\n", "\n"])
                    continue
                elif not is_header and not in_cell:
                    raise RuntimeError("Something weird happened")

    write_notebook(module.stem, cells)