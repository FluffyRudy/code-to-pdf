import os
import subprocess
from pathlib import Path

def generate_pdfs(directory):
    for file in Path(directory).glob("*.py"):
        command = ["python3", "../main.py", "--cli", "--code", str(file)]
        print(f"Generating PDF for {file}...")
        subprocess.run(command)

if __name__ == "__main__":
    generate_pdfs("../scratch")
