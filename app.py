import streamlit as st
import traceback
import zipfile
import io
import re

# IMPORTS (si fallan, el try/except lo mostrará en pantalla)
from generator import generate_certificate
from generator_idcec import generate_idcec_certificate

st.set_page_config(
    page_title="Certificate Generator",
    page_icon="📄",
    layout="centered"
)

try:
    st.title("📄 Certificate Generator")

    # =========================
    # HELPERS
    # =========================
    def clean_filename(text):
        text = text.strip().replace(" ", "_")
        return re.sub(r"[^A-Za-z0-9_]", "", text)

    def build_aia_filename(course_number, session, name):
        safe_name = clean_filename(name)
        return f"Course_{course_number}_Session{session}_{safe_name}.pdf"

    def build_idcec_filename(course_name, name):
        safe_course = clean_filename(course_name[:40])
        safe_name = clean_filename(name)
        return f"IDCEC_{safe_course}_{safe_name}.pdf"

    # =========================
    # AIA COURSES
    # =========================
    AIA_COURSES = {
        "Architectural Acoustic Design for Commercial and Institutional Spaces": "202501",
        "Specifying Baffles": "202502",
        "Acoustics and Noise Reduction": "1012025",
        "Using Biophilic Design to Enhance Individual Welfare in Commercial Environments": "2020524",
    }

    # =========================
    # IDCEC TEMPLATES
    # =========================
    IDCEC_TEMPLATES = {
        "Architectural Acoustic Design for Commercial and Institutional Spaces": "templates/idcec/architectural_acoustic_design.pdf",
        "Specifying Baffles": "templates/idcec/specifying_baffles.pdf",
        "Acoustics and Noise Reduction": "templates/idcec/acoustics_noise_reduction.pdf",
        "Using Biophilic Design to Enhance Individual Welfare in Commercial Environments": "templates/idcec/biophilic_design.pdf",
    }

    # =========================
    # TYPE + MODE
    # =========================
    certificate_type = st.selectbox("Certificate Type", ["AIA", "IDCEC"])
    mode = st.radio("Mode", ["Individual", "Batch (multiple names)"])

    # =========================
    # AIA FLOW
    # =========================
    if certificate_type == "AIA":

        selected_course = st.selectbox("Select AIA Course", list(AIA_COURSES.keys()))
        course_number = AIA_COURSES[selected_course]

        session_number = st.text_input("Session Number", value="12")
        date = st.text_input("Date (MM.DD.YY)", value="03.02.26")

        if mode == "Individual":
            person_name = st.text_input("Person Name")

            if st.button("Generate AIA Certificate"):
                if not person_name.strip():
                    st.error("⚠️ Name required")
                else:
                    data = {
                        "person_name": person_name,
                        "course_name": selected_course,
                        "course_number": course_number,
                        "session_number": session_number,
                        "date": date,
                    }

                    pdf = generate_certificate(data)
                    filename = build_aia_filename(course_number, session_number, person_name)

                    st.success("✅ Certificate generated!")

                    st.download_button(
                        "⬇️ Download Certificate",
                        pdf,
                        file_name=filename,
                        mime="application/pdf"
                    )

        else:
            names_text = st.text_area("Paste names, one per line", height=200)

            if st.button("Generate AIA Certificates ZIP"):
                names = [n.strip() for n in names_text.split("\n") if n.strip()]

                if not names:
                    st.error("⚠️ Add at least one name")
                else:
                    zip_buffer = io.BytesIO()

                    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                        for name in names:
                            data = {
                                "person_name": name,
                                "course_name": selected_course,
                                "course_number": course_number,
                                "session_number": session_number,
                                "date": date,
                            }

                            pdf = generate_certificate(data)
                            filename = build_aia_filename(course_number, session_number, name)
                            zip_file.writestr(filename, pdf.read())

                    zip_buffer.seek(0)

                    st.success("✅ ZIP ready")

                    st.download_button(
                        "⬇️ Download ZIP",
                        zip_buffer,
                        file_name="AIA_batch.zip",
                        mime="application/zip"
                    )

    # =========================
    # IDCEC FLOW
    # =========================
    else:

        selected_course = st.selectbox("Select IDCEC Course", list(IDCEC_TEMPLATES.keys()))
        template_path = IDCEC_TEMPLATES[selected_course]

        date_of_issue = st.text_input("Date of Issue", value="10.15.25")

        if mode == "Individual":
            person_name = st.text_input("Person Name")

            if st.button("Generate IDCEC Certificate"):
                if not person_name.strip():
                    st.error("⚠️ Name required")
                else:
                    data = {
                        "person_name": person_name,
                        "date_of_issue": date_of_issue,
                        "template_path": template_path,
                    }

                    pdf = generate_idcec_certificate(data)
                    filename = build_idcec_filename(selected_course, person_name)

                    st.success("✅ IDCEC certificate generated!")

                    st.download_button(
                        "⬇️ Download Certificate",
                        pdf,
                        file_name=filename,
                        mime="application/pdf"
                    )

        else:
            names_text = st.text_area("Paste names, one per line", height=200)

            if st.button("Generate IDCEC ZIP"):
                names = [n.strip() for n in names_text.split("\n") if n.strip()]

                if not names:
                    st.error("⚠️ Add at least one name")
                else:
                    zip_buffer = io.BytesIO()

                    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                        for name in names:
                            data = {
                                "person_name": name,
                                "date_of_issue": date_of_issue,
                                "template_path": template_path,
                            }

                            pdf = generate_idcec_certificate(data)
                            filename = build_idcec_filename(selected_course, name)
                            zip_file.writestr(filename, pdf.read())

                    zip_buffer.seek(0)

                    st.success("✅ ZIP ready")

                    st.download_button(
                        "⬇️ Download ZIP",
                        zip_buffer,
                        file_name="IDCEC_batch.zip",
                        mime="application/zip"
                    )

# =========================
# ERROR HANDLER (CLAVE)
# =========================
except Exception as e:
    st.error("🔥 ERROR DETECTED")
    st.text(str(e))
    st.text(traceback.format_exc())