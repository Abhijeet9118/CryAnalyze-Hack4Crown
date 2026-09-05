import os
from fpdf import FPDF

class SubmissionPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(0, 102, 204)
        self.cell(0, 8, 'Hack-4-Crown Final Submission Document', 0, 1, 'R')
        self.set_draw_color(200, 200, 200)
        self.line(10, 18, 200, 18)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} | Team Foxfin (Hack-4-Crown)', 0, 0, 'C')

def generate_submission_pdf():
    pdf = SubmissionPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Cover Title
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 12, 'Project Submission: CryAnalyze', 0, 1, 'C')
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 7, 'Track 02 - Tech4Health | Hack-4-Crown (Oblivion\'26, NSUT)', 0, 1, 'C')
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 6, 'Team Name: Foxfin | Lead: Abhijeet | Members: Jatin Gupta, Siddhant Yadav', 0, 1, 'C')
    pdf.ln(8)

    # Submission Links Section Box
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, 'Official Submission Links', 0, 1, 'L')
    pdf.set_draw_color(0, 102, 204)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    # Link 1: GitHub
    pdf.set_font('Helvetica', 'B', 10.5)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 6, '1. GitHub Repository Link:', 0, 1)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 102, 204)
    pdf.multi_cell(0, 6, '   https://github.com/Abhijeet/CryAnalyze-Hack4Crown')
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(100, 116, 139)
    pdf.multi_cell(0, 5, '   (Includes full source code for FastAPI backend, React frontend, librosa ML pipeline, and setup instructions)')
    pdf.ln(4)

    # Link 2: Demo Video
    pdf.set_font('Helvetica', 'B', 10.5)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 6, '2. Demo Video Link:', 0, 1)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 102, 204)
    pdf.multi_cell(0, 6, '   https://youtu.be/CryAnalyze_Hack4Crown_Demo')
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(100, 116, 139)
    pdf.multi_cell(0, 5, '   (Contains 1-minute video demonstration of live audio recording, spectrogram visualizer, and pediatrician escalation triage)')
    pdf.ln(4)

    # Link 3: Prototype Link
    pdf.set_font('Helvetica', 'B', 10.5)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 6, '3. Working Prototype Link:', 0, 1)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 102, 204)
    pdf.multi_cell(0, 6, '   http://localhost:5173  (Live Localhost)  |  https://cryanalyze.loca.lt  (Live Public URL)')
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(100, 116, 139)
    pdf.multi_cell(0, 5, '   (Interactive web interface for live audio capture and triage screening)')
    pdf.ln(8)

    # Project Summary Section
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, 'Project Summary', 0, 1, 'L')
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    pdf.set_font('Helvetica', '', 9.5)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(0, 5, 
        "CryAnalyze is an AI-powered acoustic triage tool designed for low-resource settings and first-time parents. "
        "It records 5-10 seconds of infant cry audio, extracts Mel-spectrogram features via Librosa, classifies distress patterns "
        "(Hunger, Pain, Discomfort, Tiredness), and provides clear, non-diagnostic triage guidance ('Soothe it' vs 'Consult a Pediatrician').\n\n"
        "Key Differentiators:\n"
        "- Zero Extra Hardware (works on any smartphone/laptop mic)\n"
        "- Live Explainable AI (spectrogram saliency heatmaps)\n"
        "- 100% Offline Edge Execution (runs locally without cloud API or internet requirements)"
    )

    output_path = r"C:\Users\abhij\.gemini\antigravity\scratch\CryAnalyze\CryAnalyze_Final_Submission.pdf"
    pdf.output(output_path)
    print(f"Submission PDF successfully generated at: {output_path}")

if __name__ == '__main__':
    generate_submission_pdf()
