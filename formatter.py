from pygments.formatters.html import HtmlFormatter
from weasyprint import HTML


# class CustomHtmlFormatter(HtmlFormatter):
#     def __init__(self, font_size="12px", *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.font_size = font_size

#     def get_style_defs(self, arg=""):
#         style_defs = super().get_style_defs()
#         custom_css = f"""
#         pre {{
#             font-size: {self.font_size};
#         }}
#         .highlight {{
#             font-size: {self.font_size};
#             margin-top: 0;
#             padding-top: 0;
#         }}
#         """
#         return style_defs + custom_css


class CustomHtmlFormatter(HtmlFormatter):
    def __init__(self, font_size="12px", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font_size = font_size

    def get_style_defs(self, arg=""):
        # Only include the font size, set color to black, and remove any styles
        custom_css = f"""
        pre {{
            font-family: monospace;
            font-size: {self.font_size}; 
            color: black;
            background-color: white;
        }}
        """
        return custom_css


class CustomHTML(HTML):
    def __init__(
        self,
        code_html: str,
        title: str = "",
        aim: str = "",
        theory: str = "",
        algorithm: str = "",
    ):

        self.full_content = f"{code_html}"

        super().__init__(string=self.full_content)

    def __str__(self):
        return self.full_content
