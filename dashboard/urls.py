
from django.urls import path

from dashboard.views import index_view, upload_files, list_rag_view, download_rag_view, delete_rag_view

urlpatterns = [
    path('',index_view,name="index"),
    path('upload',upload_files,name="upload"),
    path('list',list_rag_view,name="list_rag"),
    path('download/<int:pk>/',download_rag_view,name="download_rag"),
    path('delete/<int:pk>/',delete_rag_view,name="delete_rag"),

]
