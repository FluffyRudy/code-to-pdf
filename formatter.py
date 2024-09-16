from pygments.formatters.html import HtmlFormatter


class CustomHtmlFormatter(HtmlFormatter):
    def __init__(self, font_size="12px", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font_size = font_size

    def get_style_defs(self, arg=""):
        style_defs = super().get_style_defs()
        custom_css = f"""
        pre {{
            font-size: {self.font_size}; 
        }}
        .highlight {{
            font-size: {self.font_size}; =
        }}
        """
        return style_defs + custom_css
