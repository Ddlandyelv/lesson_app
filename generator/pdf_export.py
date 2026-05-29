"""PDF 教案导出 — 参照美术教案样本格式"""

from fpdf import FPDF
from .models import LessonData


class LessonPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("song", "", "C:/Windows/Fonts/simsun.ttc", uni=True)
        self.set_auto_page_break(auto=True, margin=20)

    def doc_title(self, text):
        self.set_font("song", "", 18)
        self.cell(0, 12, text, new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(6)

    def info(self, label, value):
        self.set_font("song", "", 11)
        self.cell(0, 7, f"{label}{value}", new_x="LMARGIN", new_y="NEXT")

    def heading(self, text):
        self.set_font("song", "", 14)
        self.ln(5)
        self.cell(0, 8, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def body(self, text):
        if not text.strip():
            return
        self.set_font("song", "", 11)
        for line in text.split("\n"):
            if not line.strip():
                continue
            self.cell(7)
            self.multi_cell(0, 6.5, line.strip())
            self.ln(0.5)

    def bullet(self, text):
        self.set_font("song", "", 11)
        self.cell(9)
        self.multi_cell(0, 6, "• " + text.strip())
        self.ln(0.5)


def export_to_pdf(data: LessonData, output_path: str):
    pdf = LessonPDF()
    pdf.add_page()

    pdf.doc_title(f"《{data.title}》教案")

    pdf.info("适用班级：", data.level or "（由教师填写）")
    pdf.info("课    时：", data.duration or "（由教师填写）")
    pdf.info("绘画材料：", data.materials or "（由教师填写）")
    pdf.ln(6)

    # 教学目标
    pdf.heading("一、教学目标")
    pdf.body(data.objectives)

    # 重难点
    pdf.heading("二、教学重难点")
    pdf.set_font("song", "", 11)
    pdf.cell(7)
    pdf.multi_cell(0, 6.5, f"【教学重点】{data.key_points}")
    pdf.ln(1)
    pdf.cell(7)
    pdf.multi_cell(0, 6.5, f"【教学难点】{data.difficult_points}")
    pdf.ln(4)

    # 教学过程
    pdf.heading("三、教学过程")
    for step in str(data.process).split("\n"):
        step = step.strip()
        if not step:
            continue
        if step.startswith("【") and "】" in step[:10]:
            pdf.set_font("song", "", 11)
            pdf.cell(7)
            pdf.multi_cell(0, 6.5, step)
            pdf.ln(1)
        else:
            pdf.body(step)

    # 课后延伸
    if data.extension.strip():
        pdf.heading("四、课后延伸")
        pdf.body(data.extension)

    # 注意事项
    if data.notes.strip():
        pdf.heading("五、注意事项")
        for line in str(data.notes).split("\n"):
            if line.strip():
                pdf.bullet(line)

    pdf.output(output_path)
