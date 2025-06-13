
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from PIL import Image
import io
import tempfile

st.set_page_config(page_title="Clean Resume Generator", page_icon="📝")
st.title("🧾 Clean & Accurate PDF Resume Generator")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Full Name", "John Doe")
    title = st.text_input("Job Title", "AIML Engineer")
with col2:
    email = st.text_input("Email", "johndoe@email.com")
    phone = st.text_input("Phone", "1234567892")

linkedin = st.text_input("LinkedIn", "linkedin.com/in/johndoe")
github = st.text_input("GitHub", "github.com/johndoe")
location = st.text_input("Location", "Hyderabad")
availability = st.text_input("Availability", "2 weeks")

profile_img = st.file_uploader("Upload Profile Photo (Optional)", type=["jpg", "jpeg", "png"])
objective = st.text_area("Career Objective", "Results-driven AI/ML Engineer...")
skills = st.text_area("Skills", "- Python\n- TensorFlow\n- PyTorch\n- BERT\n- OpenCV\n- AWS\n- Git")
experience = st.text_area("Work Experience", "AI/ML Engineer\nTech Innovations Inc. | Jan 2022 – Present\n- Developed BERT-based NLP models\n- Led YOLOv5 deployment")
education = st.text_area("Education", "M.Sc. AI, Stanford University, 2021\nB.Tech CSE, MIT, 2019")
certifications = st.text_area("Certifications", "- AWS ML Certified\n- Deep Learning Specialization\n- TensorFlow Developer Certificate")
projects = st.text_area("Projects", "Chatbot using GPT-3\nDrone with TensorFlow Lite")

def draw_section(c, label, content, y):
    if content:
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.HexColor("#004080"))
        c.drawString(50, y, f"■  {label}")
        y -= 18
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        for line in content.strip().split("\n"):
            c.drawString(60, y, line.strip())
            y -= 14
        y -= 4
    return y

def draw_contact(c, label, value, y):
    spacing = 16
    if value:
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.darkblue)
        c.drawString(50, y, label)
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.black)
        c.drawString(150, y, value)
        y -= spacing
    return y

if st.button("🚀 Generate Resume PDF"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        c = canvas.Canvas(tmp_file.name, pagesize=A4)
        width, height = A4
        y = height - 60

        if profile_img:
            img = Image.open(profile_img)
            img_io = io.BytesIO()
            img.save(img_io, format="PNG")
            img_io.seek(0)
            c.drawImage(ImageReader(img_io), width - 120, y - 40, width=60, height=60)

        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, y, name)
        y -= 20
        c.setFont("Helvetica", 12)
        c.drawString(50, y, title)
        y -= 30

        contact_lines = [f"Email: {email}", f"Phone: {phone}", f"LinkedIn: {linkedin}", f"GitHub: {github}", f"Location: {location}", f"Availability: {availability}"]
        for contact in contact_lines:
            c.setFont("Helvetica", 10)
            c.setFillColor(colors.black)
            c.drawString(50, y, contact)
            y -= 14
        y -= 8

        y = draw_section(c, "Career Objective", objective, y)
        y = draw_section(c, "Skills", skills, y)
        y = draw_section(c, "Work Experience", experience, y)
        y = draw_section(c, "Education", education, y)
        y = draw_section(c, "Certifications", certifications, y)
        y = draw_section(c, "Projects", projects, y)

        c.setFont("Helvetica", 9)
        c.setFillColor(colors.grey)
        c.drawCentredString(width / 2, 30, f"{name} – Page 1")

        c.save()

        with open(tmp_file.name, "rb") as f:
            st.download_button(
                label="📄 Download Clean PDF Resume",
                data=f,
                file_name=f"{name.lower().replace(' ', '_')}_resume.pdf",
                mime="application/pdf"
            )
