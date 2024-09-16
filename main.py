import easygui
import threading
import argparse
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from weasyprint import HTML
from hexgen import get_random_hex
import os


def syntax_highlight(code: str, language: str) -> str:
    lexer = get_lexer_by_name(language)
    formatter = HtmlFormatter(full=True, linenos=True)
    return highlight(code, lexer, formatter)


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
    extension_mapping = {
        "py": "python",
        "js": "javascript",
        "c": "c",
        "cpp": "cpp",
        "java": "java",
        "sh": "bash",
    }
    language = extension_mapping.get(file_extension[1:], None)

    if language is None:
        print(f"Error: The language '{file_extension[1:]}' is not supported.")
        return

    with open(filepath, "r") as f:
        code = f.read()

    pdf_path = f"{os.path.splitext(filepath)[0]}_{get_random_hex(8)}.pdf"
    generate_pdf(code, language, pdf_path)


def gui_mode():
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
    main()
