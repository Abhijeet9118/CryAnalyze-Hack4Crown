from fpdf import FPDF
import os

pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_font("Arial", size=11)

# Read the markdown file
with open("CryAnalyze_Complete_Guide.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    line = line.strip()
    
    # Handle Headers
    if line.startswith("# "):
        pdf.set_font("Arial", 'B', 16)
        pdf.multi_cell(0, 10, line.replace("# ", "").encode('latin-1', 'replace').decode('latin-1'))
        pdf.set_font("Arial", size=11)
        pdf.ln(5)
    elif line.startswith("## "):
        pdf.set_font("Arial", 'B', 14)
        pdf.multi_cell(0, 8, line.replace("## ", "").encode('latin-1', 'replace').decode('latin-1'))
        pdf.set_font("Arial", size=11)
        pdf.ln(3)
    elif line.startswith("### "):
        pdf.set_font("Arial", 'B', 12)
        pdf.multi_cell(0, 6, line.replace("### ", "").encode('latin-1', 'replace').decode('latin-1'))
        pdf.set_font("Arial", size=11)
        pdf.ln(2)
        
    # Handle Separators
    elif line == "---":
        pdf.ln(5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
    # Handle empty lines
    elif line == "":
        pdf.ln(3)
        
    # Handle normal text
    else:
        # Strip simple markdown formatting
        clean_line = line.replace("**", "").replace("`", "")
        if clean_line.startswith("* "):
            clean_line = "  " + clean_line.replace("* ", "- ")
        
        pdf.multi_cell(0, 6, clean_line.encode('latin-1', 'replace').decode('latin-1'))

pdf.output("CryAnalyze_Complete_Guide.pdf")
print("PDF successfully generated!")
