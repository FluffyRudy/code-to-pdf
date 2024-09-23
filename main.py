import os
import pathlib
import argparse
import logging
import threading
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor

import easygui
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from weasyprint import HTML, CSS
from hexgen import get_random_hex
from formatter import CustomHtmlFormatter
from formatter import CustomHTML

extension_mapping = {
    "py": "python",
    "js": "javascript",
    "c": "c",
    "cpp": "cpp",
    "java": "java",
    "sh": "bash",
}


def syntax_highlight(code: str, language: str) -> str:
    lexer = get_lexer_by_name(language)
    formatter = CustomHtmlFormatter(
        full=False, linenos=False, font_size="12px", style="monokai"
    )
    result = highlight(code, lexer, formatter)
    style = formatter.get_style_defs()
    return result, style


def run_code_and_capture_output(code: str, language: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{language}") as temp_file:
        temp_file.write(code.encode("utf-8"))
        temp_file.flush()

        try:
            if language == "python":
                result = subprocess.run(
                    ["python3", temp_file.name], capture_output=True, text=True
                )
            elif language == "bash":
                result = subprocess.run(
                    ["bash", temp_file.name], capture_output=True, text=True
                )
            else:
                return "Language execution not supported."

            output = result.stdout + result.stderr
        except Exception as e:
            output = str(e)

    return output


def generate_pdf(
    code: str,
    language: str,
    file_path: str = None,
    title: str = "",
    aim: str = "",
    theory: str = "",
    is_bulk: bool = False,
):
    highlighted_code, style = syntax_highlight(code, language)
    output = run_code_and_capture_output(code, language)

    terminal_html_template = f"""
    <div class="terminal">
        <span style="color: green;">rudy@rudy</span>: 
        <span style="color: white;">~/Documents/college/ai/lab$</span> 
        <span style="color: white;">python3 {title}.py</span>
        <pre style="font-family: 'Fira Code', monospace; background-color: black; color: white; padding: 0; margin: 0; white-space: pre-wrap;">{output}</pre>
        <div style="height: 20px;"></div>
        <div style="height: 20px;"></div>
    </div>
    """

    full_html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    {style}

    * {{
        margin: 0;
        padding: 0;
    }}

    body {{
        font-family: 'Fira Code', monospace;
        color: white;
        width: 100%;
    }}

    pre {{
        font-family: 'Fira Code', monospace;
        background-color: #272822; 
        color: #f8f8f2;      
        padding: 10px;      
        border-radius: 5px;
        white-space: pre-wrap !important;     
        word-wrap: break-word !important;     
    }}

    h1, h2, h3, .pr {{
        color: black;
    }}

    hr {{
        border: 1px solid #f8f8f2;
    }}

    .terminal {{
        background-color: black;
        padding: 5px;
        color: white;
        font-family: 'Fira Code', monospace;
    }}

    .terminal .prompt {{
        color: green;
    }}

    .terminal .path {{
        color: white;
    }}

    .ib {{
        display: inline-block;
    }}
    </style>
    </head>
    <body>
    <h2 class="ib">{title}:</h2>
    <p class="pr ib"><strong>{aim}</strong></p>
    
    <pre>{highlighted_code}</pre>
    
    <hr/>
    <h3>Output:</h3>
    {terminal_html_template}
    </body>
    </html>
    """

    if file_path is None:
        file_path = f"lab{title}.pdf"

    if is_bulk:
        HTML(string=full_html_content).write_pdf(file_path)
    else:
        html_instance = CustomHTML(
            code_html=full_html_content,
            title=title,
            aim=aim,
            theory=theory,
        )
        html_instance.write_pdf(file_path)

    print(f"PDF generated: {file_path}")


def cli_mode(code_filepath: str):
    if not os.path.exists(code_filepath):
        print(f"Error: The file {code_filepath} does not exist.")
        return

    with open(code_filepath, "r") as f:
        lines = f.readlines()
        title = lines[0].strip().split(": ", 1)[1]
        aim = lines[1].strip().split(": ", 1)[1]
        code = "".join(lines[2:])

    language = "python"
    generate_pdf(code=code, language=language, title=title, aim=aim)


def main():
    parser = argparse.ArgumentParser(
        description="Code to PDF converter with CLI and GUI modes."
    )
    parser.add_argument("--cli", action="store_true", help="Set to enable CLI mode.")
    parser.add_argument(
        "--code", type=str, required=True, help="File path to the code."
    )

    args = parser.parse_args()

    if args.cli and args.code:
        cli_mode(args.code)
    else:
        gui_mode()


if __name__ == "__main__":
    main()
