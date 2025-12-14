<p align="center">
<img src="https://github.com/n4gY1/docling_dashboard/blob/master/static/img/img.png" width="500" height="500" />
<h2 align="center">Docling web Dashboard (django web server)</h2>
<p align="center">Upload ppt, docx, pdf, excel etc files and download Docling generated files.</p>
</p>

# Convert pdf, docx, doc, ppt, excel to txt / md
## AI RAG - convert your document to AI knowledge RAG format
This django dashboard use docling library, convert your documents to AI RAG format for your AI model
## Preview
<p align="center">
  <img src="sample.gif" />
</p>


<p>
  Run docker or python virtual env. Required cuda and nvidia driver
</p>
<p>
  Modify title, navbar home and footbar text with <strong>site_config.py</strong>
</p>

```bash
SITE_CONFIG = {
    "title": "DOCLING RAG DASHBOARD",
    "footer_title": "DOCLING RAG DASHBOARD created by n4gY1",
    "main_menu": "DOCLING RAG DASHBOARD"
}
```


<h1>Install</h1>

```bash
git clone https://github.com/n4gy1/docling_dashboard

cd docling_dashboard

sudo docker compose build
sudo docker compose up -d

```

<h4>Web server (django) running <strong>http://localhost:8000</strong> or <strong>http://serverip:8000</strong></h4>


<h3>--Required nvidia gpu--</h3>



