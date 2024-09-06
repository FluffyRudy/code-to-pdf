import easygui
import threading
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from hexgen import get_random_hex

def handle_text_accept(e):
    e.stop()

def save_pdf(content: str, save_to: str):
    html = HTML(string=content)
    filename = f"{get_random_hex(4)}.pdf"
    html.write_pdf(save_to, font_config=FontConfiguration())
    print(content, save_to)

def main():
    text = easygui.textbox(msg="Insert HTML code", callback=handle_text_accept)
    if text:
        file_open = easygui.filesavebox(msg="enter filename", title="filemanager", default="./")
        pdf_converter_thread = threading.Thread(target=save_pdf, args=(text, file_open))
        pdf_converter_thread.start()

if __name__ == "__main__":
    main()