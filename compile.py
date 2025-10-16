import re
import subprocess
from pathlib import Path
import shutil

ROOT: Path = Path(__file__).parent
MAIN = ROOT / "main" / "main.tex"
UTILITY = ROOT / "utilities" / "utility.tex"
DELIVER = ROOT / "deliver"

def read_macro(file_path: Path, macro: str):
    with open(file_path, "r") as f:
        content = f.read()

    patterns = [
        rf"\\newcommand{{\\{macro}}}\{{(.*?)\}}", 
        rf"\\{macro}\{{(.*?)\}}"                    
    ]
    
    for pat in patterns:
        match = re.search(pat, content)
        if match:
            return match.group(1)
    return "UNKNOWN"

    
studentnumber: str = read_macro(UTILITY, "studentnumber")
currentsubject: str = read_macro(MAIN, "currentsubject").upper()
assignment: str = read_macro(MAIN, "assignmentname")

jobname = f"{currentsubject}_A{assignment}_{studentnumber}"
cmd = ["pdflatex", "-interaction=nonstopmode", f"-jobname={jobname}", MAIN.name]

subprocess.run(cmd, cwd=MAIN.parent)
subprocess.run(cmd, cwd=MAIN.parent)

output_pdf = ROOT / f"{jobname}.pdf"

generated_pdf = MAIN.parent / f"{jobname}.pdf"
if generated_pdf.exists():
    shutil.move(str(generated_pdf), output_pdf)