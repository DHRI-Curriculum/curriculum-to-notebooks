# Convert DHRI curriculum from markdown files to Jupyter notebooks

Want to run it? Simple: Just type **`python convert-to-notebooks.py`** into your terminal.

It should do two things:

1. Clone all of the DHRI curriculum into a folder inside the directory.

2. Convert each of the markdown files into code blocks (for Python code) and headers (for headers) and text blocks (for continuous paragraphs). It will also download all of the images that are hosted on GitHub, and manually search through your repository directory (`github-curricula`, *see below*) for files with the same name.

After the script has run successfully, you will have two new directories in the repository's root directory:

- **`github-curricula`**: contains all the repositories from our DHRI-Curriculum organization on your local drive.

- **`notebooks`**: contains all of the Jupyter notebook files (`.ipynb`) that can now be opened with your Jupyter Notebooks or Jupyter Lab software. Note that this directory also contains an `img` directory with all of the necessary images for all the notebooks.

## Settings

The only settings necessary are in `order.json`, a file that contains the order of the section in each module. Note: If a module does not exist in `order.json`, the module's contents will not be converted to notebooks.

The order file must be a validly formatted JSON file. (Recommendation: run it through a JSON linter before saving.)

## Current known bugs

Currently, here are the known bugs in the script that need attention:

- Something in the script still makes the *last* section in each module (specified in `order.json`) end up *first* in each notebook. It is unclear why and this needs some further investigation.
