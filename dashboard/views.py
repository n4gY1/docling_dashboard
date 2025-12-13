import multiprocessing
import os
import threading

from django.contrib import messages
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect
from dashboard.models import GeneratedRag
from dashboard.utils import save_file

# Create your views here.
def index_view(request):
    template = "dashboard/index.html"
    context = {}
    return render(request,template_name=template,context=context)

def upload_files(request):
    files = request.FILES.getlist("files")
    #print(files)

    for idx,f in enumerate(files):
        if GeneratedRag.objects.filter(filename=f.name):
            messages.error(request, f"{f.name} is already exist in the database")
            print("[!] ERROR, this file is already exist in the database")
            return redirect("index")
        try:
            rag = GeneratedRag.objects.create(
                filename=f.name
            )
            rag.save()
            file_bytes = f.read()
            print(f"[+] save to database {f.name}, pk: {rag.pk}")

            thread = threading.Thread(
                target=save_file,
                args=(file_bytes,f.name),
                daemon=True
            )
            thread.start()

            #process=multiprocessing.Process(target=save_file,args=(file_bytes,f.name),daemon=True)
            #process.start()

            #save_file(file_bytes,f.name)
        except Exception as e:
            print(f"[!] ERROR when save file to db: {e}")
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

def delete_rag_view(request,pk):
    rag = GeneratedRag.objects.get(pk=pk)
    if rag.path is not None and os.path.exists(rag.path):
        os.remove(rag.path)
    tmp_path = "/static/documents/" + rag.filename
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
    rag.delete()

    messages.success(request, "RAG AND temp File deleted successfully.")
    return redirect("list_rag")



