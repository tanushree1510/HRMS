import os
import re
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import docx

def extract_text_from_pdf(filepath: str) -> str:
    try:
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Error reading PDF {filepath}: {e}")
        return ""

def extract_text_from_docx(filepath: str) -> str:
    try:
        doc = docx.Document(filepath)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error reading DOCX {filepath}: {e}")
        return ""

def extract_text_from_txt(filepath: str) -> str:
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading TXT {filepath}: {e}")
        return ""

def extract_text(filepath: str) -> str:
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(filepath)
    elif ext == '.docx':
        return extract_text_from_docx(filepath)
    elif ext == '.txt':
        return extract_text_from_txt(filepath)
    else:
        return ""

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def screen_resumes(jd_filepath: str, resume_filepaths: List[str], threshold: float = 0.3) -> List[Tuple[str, float]]:
    jd_text = extract_text(jd_filepath)
    if not jd_text:
        return []

    jd_text = clean_text(jd_text)

    resume_texts = []
    valid_resumes = []

    for resume_path in resume_filepaths:
        resume_text = extract_text(resume_path)
        if resume_text:
            resume_texts.append(clean_text(resume_text))
            valid_resumes.append(resume_path)

    if not resume_texts:
        return []

    all_texts = [jd_text] + resume_texts

    vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    jd_vector = tfidf_matrix[0:1]
    resume_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(jd_vector, resume_vectors)[0]

    results = []
    for i, score in enumerate(similarities):
        if score >= threshold:
            results.append((valid_resumes[i], float(score)))

    results.sort(key=lambda x: x[1], reverse=True)
    return results

def get_top_matching_resumes(jd_filepath: str, resume_filepaths: List[str], top_n: int = 10) -> List[dict]:
    matches = screen_resumes(jd_filepath, resume_filepaths, threshold=0.6)
    top_matches = matches[:top_n]

    return [
        {
            "filename": os.path.basename(filepath),
            "filepath": filepath,
            "match_score": round(score * 100, 2)
        }
        for filepath, score in top_matches
    ]
