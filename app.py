import streamlit as st
from generator import generate_certificate
import zipfile
import io
import re

st.set_page_config(
    page_title="Certificate Generator",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Certificate Generator")

# =========================
# HELPERS
# =========================
def clean_filename(text):
    text = text.strip().replace(" ", "_")
    return re.sub(r'[^A-Za-z0-9_]', '', text)

def build_filename(course_number, session, name):
    safe_name = clean_filename(name)
    return f"Course_{course_number}_Session{session}_{safe_name}.pdf"

# =========================
# COURSES
# =========================
COURSES = {
    "Architectural Acoustic Design for Commercial and Institutional Spaces": "202501",
    "Specifying Baffles": "202502",
    "Acoustics and Noise Reduction": "1012025",
    "Using Biophilic Design to Enhance Individual Welfare in Commercial Environments": "2020524"
}

# =========================
# MODE
# =========================
mode = st.radio("Mode", ["Individual", "Batch (multiple names)"])

selected_course = st.selectbox("Select Course", list(COURSES.keys()))
course_number = COURSES[selected_course]

session_number = st.text_input("Session Number", value="12")
date = st.text_input("Date (MM.DD.YY)", value="03.02.26")

# =========================
# INDIVIDUAL
# =========================
if mode == "Individual":
    person_name = st.text_input("Person Name")

    if st.button("Generate Certificate"):
        if not person_name.strip():
            st.error("⚠️ Name required")
        else:
            data = {
                "person_name": person_name,
                "course_name": selected_course,
                "course_number": course_number,
                "session_number": session_number,
                "date": date
            }

            pdf = generate_certificate(data)

            filename = build_filename(course_number, session_number, person_name)

            st.download_button(
                "⬇️ Download Certificate",
                pdf,
                file_name=filename,
                mime="application/pdf"
            )

# =========================
# BATCH
# =========================
else:
    names_text = st.text_area(
        "Paste names (one per line)",
        height=200,
        placeholder="Juan Perez\nMaria Lopez\nCarlos Diaz"
    )

    if st.button("Generate Certificates (ZIP)"):
        names = [n.strip() for n in names_text.split("\n") if n.strip()]

        if not names:
            st.error("⚠️ Add at least one name")
        else:
            zip_buffer = io.BytesIO()

            progress_bar = st.progress(0)
            status_text = st.empty()

            total = len(names)

            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for i, name in enumerate(names):
                    data = {
                        "person_name": name,
                        "course_name": selected_course,
                        "course_number": course_number,
                        "session_number": session_number,
                        "date": date
                    }

                    pdf = generate_certificate(data)

                    filename = build_filename(course_number, session_number, name)

                    zip_file.writestr(filename, pdf.read())

                    # 🔥 progreso
                    progress = (i + 1) / total
                    progress_bar.progress(progress)
                    status_text.text(f"Generating {i+1}/{total} → {name}")

            zip_buffer.seek(0)

            st.success(f"✅ Generated {total} certificates")

            st.download_button(
                "⬇️ Download ZIP",
                zip_buffer,
                file_name=f"Course_{course_number}_Session{session_number}.zip",
                mime="application/zip"
            )