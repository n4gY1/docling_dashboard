import datetime

import os

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
    #generate_rag(filename=filename)

def generate_rag(filename):

    print("generate RAG",filename)
    source = DOCUMENT_PATH + filename
    converter = DocumentConverter()
    result = converter.convert(source)
    result_txt = result.document.export_to_markdown()
    rag_filename = DOCUMENT_PATH + "RAG/" + filename + ".md"
    rag = GeneratedRag.objects.get(filename=filename)

    try :
        with open (rag_filename,"w",encoding="utf-8") as document:
            document.write(result_txt)
        print(f"[+] {rag_filename} RAG is saved")

        rag.finished_at = datetime.datetime.now()
        rag.path = rag_filename
        rag.lines = len(result_txt.splitlines())
        rag.content = result_txt[0:145]
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


