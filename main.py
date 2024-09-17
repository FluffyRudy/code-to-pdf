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
    formatter = CustomHtmlFormatter(full=True, linenos=False, font_size="12px")
    result = highlight(code, lexer, formatter)
    return result


def generate_pdf(code: str, language: str, file_path: str = None):
    highlighted_code = syntax_highlight(code, language)
    if file_path is None:
        file_path = f"code_{get_random_hex(8)}.pdf"
    HTML(string=highlighted_code).write_pdf(file_path)
    print(f"PDF generated: {file_path}")


def cli_mode(filepath: str):
    if not os.path.exists(filepath):
        print(f"Error: The file {filepath} does not exist.")
        return

    _, file_extension = os.path.splitext(filepath)
    language = extension_mapping.get(file_extension[1:], None)

    if language is None:
        print(f"Error: The language '{file_extension[1:]}' is not supported.")
        return

    with open(filepath, "r") as f:
        code = f.read()

    pdf_path = f"{os.path.splitext(filepath)[0]}_{get_random_hex(8)}.pdf"
    generate_pdf(code, language, pdf_path)


def generate_from_file(path: pathlib.Path):
    with open(path) as f:
        code = f.read()
        pdf_path = f"./{path.stem}.pdf"
        _, file_extension = os.path.splitext(path)
        language = extension_mapping.get(file_extension[1:], None)
        if language is None:
            logging.warning("Language doesnt exist in mapping")
            return
        generate_pdf(code, language, file_path=pdf_path)


def gui_mode():
    modes = ("copypaste", "bulkfiles")
    mode = easygui.choicebox("Select mode: ", choices=modes)
    if mode == "bulkfiles":
        directory = easygui.diropenbox(
            msg="Choose directory to perform operation",
            title="Choose Directory",
        )

        if directory is None:
            easygui.msgbox("No directory selected, exiting.")
            return

        filtered_files = []
        for file in pathlib.Path(directory).iterdir():
            if file.suffix[1:] in extension_mapping.keys():
                filtered_files.append(file)

        easygui.msgbox(
            msg="\n".join([str(file) for file in filtered_files]),
            ok_button="Proceed",
        )

        with ThreadPoolExecutor(max_workers=4) as executor:
            for file in filtered_files:
                executor.submit(generate_from_file, file)

        return

    languages = ["python", "javascript", "c", "cpp", "java", "bash"]
    language = easygui.choicebox("Select programming language:", choices=languages)
    if not language:
        easygui.msgbox("No language selected, exiting.")
        return

    code = easygui.textbox(f"Insert your {language} code here:")
    if not code:
        easygui.msgbox("No code provided, exiting.")
        return

    threading.Thread(target=generate_pdf, args=(code, language)).start()


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
