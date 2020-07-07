from django import forms
from django.http import HttpResponse
from django.shortcuts import render

from . import util
import random
try:
    import markdown2 as md
except ImportError:
    if settings.DEBUG:
        raise template.TemplateSyntaxError("Error in {% markdown %} filter: The python-markdown2 library isn't installed.")

class SForm(forms.Form):
    q = forms.CharField(label='Search Encyclopedia', max_length=50)

class NewForm(forms.Form):
    title = forms.CharField(label="Title", max_length=50)
    text = forms.CharField(label="Content:", widget=forms.Textarea(attrs={"rows":25, "cols":20}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
         "form": SForm()
    })

def read_entry(request, title):
        entry = util.get_entry(title)
        if entry:
            request.session["title"] = title
            request.session["entry"] = entry
            return render(request, "encyclopedia/md.html", {
            "entry": markdown(entry),
            "title": title
            })
        return render(request, "encyclopedia/err.html", {
        "message": "Page Not Found"
})
def s_sub(request):
    if request.method == "POST":
        form = SForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data["q"]
            entries = util.list_entries()
            if q in entries:
                return render(request, "encyclopedia/md.html", {
                    "entry": markdown(util.get_entry(q)),
                    "title": q
                })
            else:
                sstring = []
                for entry in entries:
                    lentry = entry.lower()
                    if lentry.find(q.lower()) != -1:
                        sstring.append(entry)
                return render(request, "encyclopedia/index.html", {
                    "entries": sstring,
                    "form": form
                })
        return render(request, "encyclopedia/subs.html", {
            "q": form
            })
    else:
        form = SForm()

def add(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            if util.get_entry(title):
                return render(request, "encyclopedia/err.html", {
                    "message": "Entry already Exist - Use EDIT"
                })
            else:
                util.save_entry(title, text)
                return render(request, "encyclopedia/add.html",{
                    "form": SForm(),
                    "form2": NewForm()
                })
    return render(request, "encyclopedia/add.html", {
        "form": SForm(),
        "form2": NewForm (initial={"title": "Entry Name", "text": "#Title\n\nContent"})
    })

def edit(request):
    data = {"title": request.session["title"],
            "text": request.session["entry"]
            }
    f = NewForm(data)
    return render(request, "encyclopedia/edit.html", {
        "form2": f
    })

def save(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title = request.session["title"]
            text = form.cleaned_data["text"]
            util.save_entry(title, text)
            return render(request, "encyclopedia/md.html", {
                "form": SForm(),
                "title": request.session["title"],
                "entry": markdown(text)
                })

def rand(request):
    entries = util.list_entries()
    title = random.choices(entries)
    title = title[0]
    entry = util.get_entry(title)
    return render(request, "encyclopedia/md.html", {
        "entry": markdown(entry),
        "title": title
    })

def markdown(value):
    return md.markdown(value)



