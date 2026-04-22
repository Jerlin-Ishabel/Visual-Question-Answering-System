from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO
from datetime import datetime
import os


# =====================================================
# PROJECT PATH
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_DIR = os.path.join(BASE_DIR, "assets")


# =====================================================
# FONT FILES (Make sure these exist inside assets)
# =====================================================
FONT_MAP = {
    "English": "NotoSans-Regular.ttf",
    "Hindi": "NotoSansDevanagari-Regular.ttf",
    "Tamil": "NotoSansTamil-Regular.ttf",
    "Malayalam": "NotoSansMalayalam-Regular.ttf",
    "Telugu": "NotoSansTelugu-Regular.ttf",
}


# =====================================================
# LABELS (Selected Language)
# =====================================================
LABELS = {
    "English": {
        "title": "Visual Question Answering Report",
        "image": "Input Image",
        "question": "Question",
        "gradcam": "Grad-CAM",
        "time": "Generated On"
    },
    "Hindi": {
        "title": "दृश्य प्रश्न उत्तर रिपोर्ट",
        "image": "इनपुट चित्र",
        "question": "प्रश्न",
        "gradcam": "ग्रेड-कैम",
        "time": "निर्माण समय"
    },
    "Tamil": {
        "title": "காட்சி கேள்வி பதில் அறிக்கை",
        "image": "உள்ளீட்டு படம்",
        "question": "கேள்வி",
        "gradcam": "கிராட்-காம்",
        "time": "உருவாக்கப்பட்ட நேரம்"
    },
    "Malayalam": {
        "title": "വിഷ്വൽ ചോദ്യ ഉത്തര റിപ്പോർട്ട്",
        "image": "ഇൻപുട്ട് ചിത്രം",
        "question": "ചോദ്യം",
        "gradcam": "ഗ്രാഡ്-കാം",
        "time": "സൃഷ്ടിച്ച സമയം"
    },
    "Telugu": {
        "title": "విజువల్ ప్రశ్న సమాధాన నివేదిక",
        "image": "ఇన్‌పుట్ చిత్రం",
        "question": "ప్రశ్న",
        "gradcam": "గ్రాడ్-క్యామ్",
        "time": "సమయం"
    }
}


# =====================================================
# SAFE FONT REGISTRATION
# =====================================================
def register_font(language):
    font_file = FONT_MAP.get(language, FONT_MAP["English"])
    font_path = os.path.join(ASSET_DIR, font_file)

    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font missing: {font_file}")

    font_name = f"Font_{language}"

    if font_name not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(font_name, font_path))

    return font_name


# =====================================================
# MAIN FUNCTION
# =====================================================
def generate_pdf(image, qa_list=None, heatmap_path=None, language="English"):

    if language not in LABELS:
        language = "English"

    # Register selected language font
    selected_font = register_font(language)

    # Register English font separately for question text
    english_font = register_font("English")

    LABEL = LABELS[language]
   # ✅ Use PROJECT ROOT reports folder safely
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORT_DIR = os.path.join(PROJECT_ROOT, "reports")

    os.makedirs(REPORT_DIR, exist_ok=True)  # Create if not exists

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"VQA_Report_{language}_{timestamp}.pdf"
    file_path = os.path.join(REPORT_DIR, file_name)


    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    elements = []

    # =====================================================
    # STYLES
    # =====================================================
    title_style = ParagraphStyle(
        name="TitleStyle",
        fontName=selected_font,
        fontSize=20,
        alignment=1,
        textColor=colors.HexColor("#4f46e5"),
        spaceAfter=6
    )

    time_style = ParagraphStyle(
        name="TimeStyle",
        fontName=selected_font,
        fontSize=10,
        alignment=1,
        spaceAfter=20
    )

    section_style = ParagraphStyle(
        name="SectionStyle",
        fontName=selected_font,
        fontSize=14,
        textColor=colors.HexColor("#2563eb"),
        spaceAfter=4
    )

    question_style = ParagraphStyle(
        name="QuestionStyle",
        fontName=english_font,  # Always English
        fontSize=12,
        leading=16,
        spaceAfter=6
    )

    answer_style = ParagraphStyle(
        name="AnswerStyle",
        fontName=selected_font,
        fontSize=12,
        leading=18
    )

    # =====================================================
    # TITLE
    # =====================================================
    elements.append(Paragraph(LABEL["title"], title_style))
    elements.append(
        Paragraph(
            f"{LABEL['time']}: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
            time_style
        )
    )

    # =====================================================
    # INPUT IMAGE
    # =====================================================
    elements.append(Paragraph(LABEL["image"], section_style))
    elements.append(Spacer(1, 6))

    img_buffer = BytesIO()
    image.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    elements.append(Image(img_buffer, width=4.8 * inch, height=3.5 * inch))
    elements.append(Spacer(1, 20))

    # =====================================================
    # Q&A SECTION
    # =====================================================
    if qa_list:
        for idx, qa in enumerate(qa_list, 1):

            # Question label
            elements.append(
                Paragraph(f"{LABEL['question']} {idx}", section_style)
            )

            # Question text (Always English)
            elements.append(
                Paragraph(qa["question"], question_style)
            )

            # Answer box
            answer_table = Table(
                [[Paragraph(qa["answer"], answer_style)]],
                colWidths=[doc.width]
            )

            answer_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fef3c7")),
                ("BOX", (0, 0), (-1, -1), 1, colors.orange),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]))

            elements.append(answer_table)
            elements.append(Spacer(1, 18))

    # =====================================================
    # GRAD-CAM SECTION
    # =====================================================
    if heatmap_path and os.path.exists(heatmap_path):

        elements.append(Spacer(1, 10))
        elements.append(Paragraph(LABEL["gradcam"], section_style))
        elements.append(Spacer(1, 6))

        elements.append(
            Image(heatmap_path, width=4.8 * inch, height=3.5 * inch)
        )

    # =======================
    # BUILD
    # =======================
    doc.build(elements)
    buffer.seek(0)

    pdf_bytes = buffer.getvalue()

    # ✅ Save automatically in reports folder
    with open(file_path, "wb") as f:
        f.write(pdf_bytes)

    print("PDF saved at:", file_path)

    return pdf_bytes, file_name