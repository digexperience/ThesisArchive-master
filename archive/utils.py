import pdfplumber
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.conf import settings
from django.core.mail import send_mail


def test_send(subject, message, recipients):
	send_mail(
    		subject=subject,
    		message=message,
    		from_email=settings.DEFAULT_FROM_EMAIL,
    		recipient_list=recipients)

def send_email(subject, message, recipients):
	send_mail(
    		subject=subject,
    		message=message,
    		from_email=settings.DEFAULT_FROM_EMAIL,
    		recipient_list=recipients)

def contact_us(message, sender):
	send_mail(
    		subject="Contact Us",
    		message=message,
    		from_email=sender,
    		recipient_list=list(settings.EMAIL_HOST_USER))

def send_email_token(email, token, host):
	try:
		print("send email")
		subject = 'Welcome to Thesis Archive! Verify your email address.'
		message = f'Click on the link Verify https://{host}/verify/{str(token)}'
		from_email = settings.DEFAULT_FROM_EMAIL
		recipient_list = [email, ]
		send_mail(subject, message, from_email, recipient_list)
	except Exception as e:
		return False
	
	return True

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs]).strip()

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    return ""

def compare_documents(file1_path, file2_path):
    text1 = extract_text(file1_path)
    text2 = extract_text(file2_path)

    if not text1 or not text2:
        return "One or both documents could not be processed."

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    return f"Similarity Score: {similarity:.2f}. Higher means more similar."