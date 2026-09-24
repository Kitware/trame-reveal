from pathlib import Path

from trame_reveal import __version__

serve_path = str(Path(__file__).with_name("serve").resolve())
serve_directory = f"__trame_revealjs_{__version__}"

serve = {serve_directory: serve_path}
scripts = [f"{serve_directory}/trame_revealjs.umd.js"]
styles = [serve_directory + "/style.css"]
vue_use = ["trame_revealjs"]
