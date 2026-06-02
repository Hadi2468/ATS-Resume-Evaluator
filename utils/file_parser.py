import pdfplumber
import docx2txt

def extract_text(uploaded_file):

    if uploaded_file.name.endswith(".pdf"):

        with pdfplumber.open(uploaded_file) as pdf:

            return "\n".join(
                page.extract_text() or ""
                for page in pdf.pages
            )

    elif uploaded_file.name.endswith(".docx"):

        return docx2txt.process(uploaded_file)

    else:

        raise ValueError(
            "Unsupported file format"
        )