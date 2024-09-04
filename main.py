from typing import Optional
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from pathlib import Path
from hexgen import get_random_hex


class Html2Pdf:
    def __init__(self, html: str, css: Optional[str] = None):
        html_path = Path(html)
        css_path = Path(css) if css is not None else None

        if not html_path.exists():
            raise FileNotFoundError("html file doesnt exist")
        if css is not None and not css_path.exists():
            raise FileExistsError("Css file doesnt exist")

        self.html_instance: HTML = HTML(filename=html)
        if css is not None:
            self.css_instance: CSS = CSS(filename=css)
        else:
            self.css_instance: CSS = CSS(string="")
        self.font_config = FontConfiguration()

    def make_pdf(self, path: str = "."):
        save_path = Path(path).resolve()

        if save_path.is_dir():
            filename = str(get_random_hex(4)) + ".pdf"
            save_path = save_path.joinpath(filename)

        try:
            self.html_instance.write_pdf(
                save_path, font_config=self.font_config, stylesheets=[self.css_instance]
            )
        except Exception as error:
            print(error)


if __name__ == "__main__":
    Html2Pdf("./sample.html", "./sample.css").make_pdf()
