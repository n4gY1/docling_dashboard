import datetime
import os
import threading

from django.contrib import messages
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect
from docling.document_converter import DocumentConverter

from dashboard.models import GeneratedRag

documents_path = "static/documents/"

def save_file(data,filename):
    p = documents_path + filename
    with open (p,"wb+") as document:
        for chunk in data.chunks():
            document.write(chunk)

    threading.Thread(
        target=generate_rag,
        args=(filename),
        daemon=True
    ).start()
    #generate_rag(filename=filename)

def generate_rag(filename):
    #print("generate RAG",file)
    source = documents_path + filename
    converter = DocumentConverter()
    result = converter.convert(source)
    result_txt = result.document.export_to_markdown()

    rag_filename = documents_path + "RAG/" + filename + ".md"
    with open (rag_filename,"w",encoding="utf-8") as document:
        document.write(result_txt)
    print(f"[+] {rag_filename} RAG is saved")

    rag = GeneratedRag.objects.get(filename=filename)
    rag.finished_at = datetime.datetime.now()
    rag.path = rag_filename
    rag.lines = len(result_txt.splitlines())
    rag.content = result_txt[0:145]
    rag.save()

    print(f"[+] modified rag finished_at {rag.pk}")

    remove_file(filename=filename)


def remove_file(filename):
    print(f"[+] remove temp file {filename}")
    os.remove(f"{documents_path}/{filename}")



# Create your views here.
def index_view(request):
    template = "dashboard/index.html"
    context = {}
    return render(request,template_name=template,context=context)


def upload_files(request):
    files = request.FILES.getlist("files")
    #print(files)

    for idx,f in enumerate(files):
        rag = GeneratedRag.objects.create(
            filename=f.name
        )
        rag.save()
        print(f"[+] save to database {f.name}, pk: {rag.pk}")
        save_file(f,f.name)


        #save_file(data=f,filename=str(idx)+"_"+f.name)

    messages.success(request,"File uploads and generate RAG is running in the background... Please wait")
    return redirect("index")

def list_rag_view(request):
    template = "dashboard/list_rag.html"
    rags = GeneratedRag.objects.filter(finished_at__isnull=False)
    rags_not_success = GeneratedRag.objects.filter(finished_at__isnull=True)

    context = {
        "rags":rags,
        "rags_not_success":rags_not_success
    }
    return render(request, template_name=template, context=context)

def download_rag_view(request,pk):
    rag = GeneratedRag.objects.get(pk=pk)
    download_url = rag.path

    if not os.path.exists(download_url):
        return HttpResponse("File not found :(")

    file_handle = open(download_url,"rb")

    print(f"[+] downloaded path : {download_url}")
    return FileResponse(file_handle,as_attachment=True)
