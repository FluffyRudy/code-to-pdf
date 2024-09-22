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
    </div>
    """

    full_html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    {style}

    body {{
        font-family: 'Fira Code', monospace;
        color: white;
        padding: 20px;
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

    h3 {{
        color: white;
    }}

    hr {{
        border: 1px solid #f8f8f2;
    }}

    .terminal {{
        background-color: black;
        padding: 10px;
        color: white;
        font-family: 'Fira Code', monospace;
    }}

    .terminal .prompt {{
        color: green;
    }}

    .terminal .path {{
        color: white;
    }}
    </style>
    </head>
    <body>
    {aim and f"<h2 style='display: inline-block;'>{title}:&nbsp;</h2><p style='display: inline-block;'><strong>{aim}</strong></p>"}
    
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


def cli_mode(code_filepath: str, title: str, aim: str):
    if not os.path.exists(code_filepath):
        print(f"Error: The file {code_filepath} does not exist.")
        return

    language = "python"

    with open(code_filepath, "r") as f:
        code = f.read()

    pdf_path = f"lab{title}.pdf"
    generate_pdf(code, language, pdf_path, title, aim)


def generate_from_file(path: pathlib.Path):
    with open(path) as f:
        code = f.read()
        pdf_path = f"./{path.stem}.pdf"
        language = "c"
        generate_pdf(code, language, file_path=pdf_path)


def gui_mode():
    modes = "copypaste"
    mode = modes

    if mode == "bulkfiles":
        directory = easygui.diropenbox(
            msg="Choose directory to perform operation",
            title="Choose Directory",
        )

        if directory is None:
            easygui.msgbox("No directory selected, exiting.")
            return

        filtered_files = [
            file
            for file in pathlib.Path(directory).iterdir()
            if file.suffix[1:] in extension_mapping.keys()
        ]

        easygui.msgbox(
            msg="\n".join([str(file) for file in filtered_files]),
            ok_button="Proceed",
        )

        with ThreadPoolExecutor(max_workers=4) as executor:
            for file in filtered_files:
                executor.submit(generate_from_file, file)

        return

    elif mode == "copypaste":
        language = "python"

        code = easygui.textbox(f"Insert your {language} code here:")
        if not code:
            return

        title = easygui.enterbox("Enter the title (optional):")
        aim = easygui.textbox("Insert the aim of this code (2-3 lines):")
        theory = ""

        threading.Thread(
            target=generate_pdf,
            args=(code, language, None, title, aim, theory, False),
        ).start()


def main():
    parser = argparse.ArgumentParser(
        description="Code to PDF converter with CLI and GUI modes."
    )
    parser.add_argument("--cli", action="store_true", help="Set to enable CLI mode.")
    parser.add_argument(
        "--code", type=str, required=True, help="File path to the Python code."
    )
    parser.add_argument("--title", type=str, required=True, help="Title for the code.")
    parser.add_argument("--aim", type=str, required=True, help="Aim of the code.")

    args = parser.parse_args()

    if args.cli and args.code and args.title and args.aim:
        cli_mode(args.code, args.title, args.aim)
    else:
        gui_mode()


if __name__ == "__main__":
    main()
