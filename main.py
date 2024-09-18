import os
import pathlib
import argparse
import logging
import threading
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
    formatter = CustomHtmlFormatter(full=False, linenos=False, font_size="12px")
    result = highlight(code, lexer, formatter)
    style = formatter.get_style_defs()
    return result, style


def generate_pdf(
    code: str,
    language: str,
    file_path: str = None,
    title: str = "",
    aim: str = "",
    theory: str = "",
    algorithm: str = "",
    is_bulk: bool = False,
):
    highlighted_code, style = syntax_highlight(code, language)
    full_html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>{style}</style>
    </head>
    <body>
    {title and f"<h1 style='text-align:center;'>Experiment NO.{title}</h1>"}
    {aim and f"<h2>Aim:</h2><p style='font-family:monospace;'>{aim}</p>"}
    {theory and f"<h2>Theory:</h2><p style='font-family:monospace;'>{theory}</p>"}
    {algorithm and f"<h2>Algorithm:</h2><p style='font-family:monospace;'>{algorithm}</p>"}
    <h2>Code</h2>
    <pre style='font-family:monospace;'>{highlighted_code}</pre>
    </body>
    </html>
    """

    if file_path is None:
        file_path = f"code_{get_random_hex(8)}.pdf"

    if is_bulk:
        HTML(string=full_html_content).write_pdf(file_path)
    else:
        html_instance = CustomHTML(
            code_html=full_html_content,
            title=title,
            aim=aim,
            theory=theory,
            algorithm=algorithm,
        )
        html_instance.write_pdf(file_path)

    print(f"PDF generated: {file_path}")


def cli_mode(filepath: str):
    if not os.path.exists(filepath):
        print(f"Error: The file {filepath} does not exist.")
        return

    # Set language to C for temporary testing
    language = "c"

    with open(filepath, "r") as f:
        code = f.read()

    pdf_path = f"{os.path.splitext(filepath)[0]}_{get_random_hex(8)}.pdf"
    generate_pdf(code, language, pdf_path)


def generate_from_file(path: pathlib.Path):
    with open(path) as f:
        code = f.read()
        pdf_path = f"./{path.stem}.pdf"
        # Set language to C for temporary testing
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
        # Set language to C for temporary testing
        language = "c"

        code = easygui.textbox(f"Insert your {language} code here:")
        if not code:
            # easygui.msgbox("No code provided, exiting.")
            return

        title = easygui.enterbox("Enter the title (optional):")
        aim = easygui.textbox("Insert the aim of this code (2-3 lines):")
        theory = easygui.textbox("Insert the theory behind the code (6-10 lines):")
        algorithm = easygui.textbox(
            "Insert the algorithm or steps (any number of lines):"
        )

        threading.Thread(
            target=generate_pdf,
            args=(code, language, None, title, aim, theory, algorithm, False),
        ).start()


def main():
    parser = argparse.ArgumentParser(
        description="Code to PDF converter with CLI and GUI modes."
    )
    parser.add_argument(
        "--cli", type=bool, default=False, help="Set to True for CLI mode."
    )
    parser.add_argument("--path", type=str, help="File path for CLI mode input.")

    args = parser.parse_args()

    if args.cli and args.path:
        cli_mode(args.path)
    else:
        gui_mode()


if __name__ == "__main__":
    """user --cli=True path=/path/<filename>.{py,c,cpp,java,sh,js}"""
    main()
