
import os
import zipfile
from io import BytesIO

from django.utils import timezone
from docling.document_converter import DocumentConverter

from dashboard.models import GeneratedRag

DOCUMENT_PATH = "static/documents/"

def save_file(data,filename):
    p = DOCUMENT_PATH + filename
    try:
        with open (p,"wb+") as document:
            document.write(data)
        generate_rag(filename=filename)
    except Exception as e:
        print(f"[!] ERROR when upload the file to the documents directory, {e}")
        rag = GeneratedRag.objects.get(filename=filename)
        rag.errors = str(e)
        rag.save()
    #generate_rag(filename=filename)

def generate_rag(filename):
    error = ""

    print("generate RAG",filename)
    source = DOCUMENT_PATH + filename
    try:
        converter = DocumentConverter()
        result = converter.convert(source)
        result_txt = result.document.export_to_markdown()
    except Exception as e:
        error = str(e)
        raise str(e)
    rag_filename = DOCUMENT_PATH + "RAG/" + filename + ".md"
    rag = GeneratedRag.objects.get(filename=filename)

    try :
        with open (rag_filename,"w",encoding="utf-8") as document:
            document.write(result_txt)
        print(f"[+] {rag_filename} RAG is saved")

        rag.finished_at = timezone.now()
        rag.path = rag_filename
        rag.lines = len(result_txt.splitlines())
        rag.content = result_txt[0:145]
        rag.errors = error
        rag.save()
        print(f"[+] modified rag finished_at {rag.pk}")

        remove_file(filename=filename)
    except Exception as e:
        print(f"[!] ERROR when modified rag finished_at rag.pk , e")
        rag.errors = f"{e}"
        rag.save()

def remove_file(filename):
    print(f"[+] remove temp file {filename}")
    os.remove(f"{DOCUMENT_PATH}/{filename}")



###### ZIP
def create_rag_zip():
    rag_dir = DOCUMENT_PATH + "RAG/"
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for filename in os.listdir(rag_dir):
            file_path = os.path.join(rag_dir, filename)
            if os.path.isfile(file_path):
                zipf.write(file_path, filename)
    buffer.seek(0)
    return buffer


