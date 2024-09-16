# Code to PDF Converter

This tool converts source code into a syntax-highlighted PDF using either a command-line interface (CLI) or a graphical user interface (GUI). It supports several popular programming languages such as Python, JavaScript, C, C++, Java, and Bash.

## Usage

### CLI Mode

To use the CLI mode, pass the `--cli=True` argument along with the `--path` argument pointing to the source code file you want to convert.

#### Example:

```bash
python main.py --cli=True --path=/path/to/your/codefile.{py,c,cpp,java,sh,js}
```
**You can add more language if you need**

To use gui mode simply run `python3 main.py`, select language, paste code and press enter and file will be saved
