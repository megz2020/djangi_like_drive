from django.views.generic import View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from forms.doc_forms import DocumentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from core.models import Document
import slate3k as slate
import re
import os

def search(files, search_term, **kwargs):
    result = []
    for file in files:
        try:
            file_path =os.path.join('media',file[0])
            with open(file_path,'rb') as f:
                extracted_text = slate.PDF(f)
                res = re.search(search_term, extracted_text[0])

                if res:
                    result += [file[0]]

        except Exception as e:
            print(e)
            return None
    return result


def home(request):
    documents = Document.objects.all()
    query = request.GET.get("q")
    if query:
        documents = documents.filter(title__icontains=query)
        if not documents :
            documents = list(Document.objects.all().values_list("document"))
    
            file = search(documents, query)
            print(file)
            documents = Document.objects.all().filter(document__in = file)


    return render(request, 'home.html', { 'documents': documents })




class FileUploadView(View):
    form_class = DocumentForm
    success_url = reverse_lazy('home')
    template_name = 'file_upload.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
        
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit = False) 
            obj.user = request.user; 
            obj.save() 
            form = self.form_class() 
    
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})
