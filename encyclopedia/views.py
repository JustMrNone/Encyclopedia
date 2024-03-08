from random import choice
from django.shortcuts import render, redirect
from markdown2 import markdown
from . import util
from django.http import HttpResponse
import os
def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    content = util.get_entry(title.strip())
    if content is None:
        content = "<h1>Error: Page Not Found</h1>"
    content = markdown(content)
    return render(request, "encyclopedia/entry.html", {"title": title, "entry": content})


def search(request):
    q = request.POST.get('q').strip()
    if q in util.list_entries():
        return redirect("entry", title=q)
    return render(request, "encyclopedia/search.html", {"entries": util.search(q), "q": q})


def create(request):
    try:
        if request.method == "POST":
            title = request.POST.get("title").strip()
            content = request.POST.get("content").strip()
            if title in util.list_entries():
                return render(request, "encyclopedia/create.html", {"error": "Page already exists!"})
            elif title == "" or content == "":
                return render(request, "encyclopedia/create.html", {"error": "Title and content are required!"})
            util.save_entry(title, content)
            return redirect("entry", title=title)
        return render(request, "encyclopedia/create.html")
    except Exception as e:
        return render(request, "encyclopedia/create.html", {'error': str(e)})

def edit(request, title):
    try:
        content = util.get_entry(title.strip())
        if content is None:
            return render(request, "encyclopedia/edit.html", {'error': "Page Not Found"})
        if request.method == "GET":
            content = request.GET.get("content").strip()
            if content == "":
                return render(request, "encyclopedia/edit.html",
                            {"message": "Can't save with empty field.", "title": title, "content": content})
            util.save_entry(title, content)
            return redirect("entry", title=title)
        return render(request, "encyclopedia/edit.html", {'content': content, 'title': title})
    except Exception as e:
        return render(request, "encyclopedia/edit.html", {'error': str(e)})


def random(request):
    entries = util.list_entries()
    return redirect("entry", title=choice(entries))

def delete_entry(request):
    if request.method == 'POST':
        entry_title = request.POST.get('entry_title')
        util.delete_entry(entry_title)  # Assuming you have a delete_entry function in util module
        return redirect('index')  # Redirect to the page displaying all entries
    else:
        return HttpResponse('Method Not Allowed', status=405)
    
