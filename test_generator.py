from generator import generate_certificate

data = {
    "person_name": "Test User",
    "course_name": "Specifying Baffles",
    "course_number": "202502",
    "session_number": "12",
    "date": "03.02.26",
    "credits": "1LU/HSW",
    "format": "In Person",
    "provider": "EzoBord",
    "instructor": "Doug Barlett"
}

pdf = generate_certificate(data)

with open("test.pdf", "wb") as f:
    f.write(pdf.read())