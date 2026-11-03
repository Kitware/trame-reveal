import logging
import re
import urllib.request
from argparse import ArgumentParser
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def fetch(url: str, target_path: Path) -> None:
    with urllib.request.urlopen(url) as response:
        content = response.read()

    with target_path.open("wb") as f:
        f.write(content)


def resolve(css_path: Path, target_dir: Path, source_url: str | None = None) -> None:
    """
    Resolve import URL in css_path by fetching and saving their content in target_dir
        source_url is used for recursive fetching
    """
    with css_path.open("r") as f:
        style = f.read()
    urls = re.findall(
        r'url\(["\']([^"\']*)["\']\)',  # URL import pattern
        style,
    )
    for url in urls:
        url_parts = url.split("/")
        name = url_parts[-1]
        base_url = "/".join(url_parts[:-1])
        target_path = target_dir.joinpath(name)
        logger.info("Fetching %s to %s")
        fetched_url = url
        if source_url is not None:
            fetched_url = source_url + "/" + url
            if not base_url:
                base_url = source_url
        fetch(fetched_url, target_path)
        style = style.replace(url, name)
        if target_path.suffix == ".css":
            resolve(target_path, target_dir, base_url)
    if source_url is None:
        # Finally rewrite updated style back
        target_path = target_dir.joinpath("style.css")
        logger.info("Writing static CSS to %s")
        with target_path.open("w") as f:
            f.write(style)


def clean_slides_files(
    html_path: str,
    css_path: str,
    target_html_path: str,
    target_css_path: str,
    static: bool = False,
):
    html_path = Path(html_path)
    if not html_path.exists():
        error = f"{html_path.as_posix()} does not exist."
        raise FileNotFoundError(error)
    if html_path.suffix != ".html":
        error = "html_path must end in .html"
        raise Exception(error)

    css_path = Path(css_path)
    if not css_path.exists():
        error = f"{css_path.as_posix()} does not exist."
        raise FileNotFoundError(error)
    if css_path.suffix != ".css":
        error = "css_path must end in .cs"
        raise Exception(error)

    css_parent_dir = css_path.parent
    css_parent_dir.mkdir(exist_ok=True, parents=True)

    with html_path.open("r") as f:
        html = f.read()

    with css_path.open("r") as f:
        css = f.read()

    clean_html = re.sub(
        r"<iframe[^>]* data-src=\"http://trame:([^\"]*)\"(?:(?!iframe).)*iframe>",
        r"<reveal-trame-app name='\g<1>' />",
        html,
    )

    clean_css = re.sub(
        r"<style>([\s\S]*)</style>",
        r"\g<1>",
        css,
    )

    with Path(target_html_path).open("w") as f:
        f.write(clean_html)

    with Path(target_css_path).open("w") as f:
        f.write(clean_css)

    if static:
        resolve(Path(target_css_path), css_parent_dir)

    logger.info("Done")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("html_path", type=str, help="Path to HTML file to be parsed")
    parser.add_argument("css_path", type=str, help="Path to CSS file to be parsed")
    parser.add_argument(
        "target_html_path",
        type=str,
        help="Path where the resulting HTML file will be written",
    )
    parser.add_argument(
        "target_css_path",
        type=str,
        help="Path where the resulting CSS file will be written",
    )
    parser.add_argument(
        "--static",
        action="store_true",
        help="Whether to resolve all URL imports in the CSS file",
    )

    args = parser.parse_args()
    clean_slides_files(
        args.html_path,
        args.css_path,
        args.target_html_path,
        args.target_css_path,
        args.static,
    )
