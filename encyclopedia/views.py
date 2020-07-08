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
    text = forms.CharField(label="Content:", widget=forms.Textarea(attrs={"rows":15, "cols":80}))

err1 = "PAGE NOT FOUND (404)"
err2 = "BAD REQUEST - PAGE ALREADY EXISTS (400)"

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
            "title": title,
            "form": SForm(),
            })
        return render(request, "encyclopedia/err.html", {
            "form": SForm(),
            "message": err1
        })

def s_sub(request):
    if request.method == "POST":
        form = SForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data["q"]
            entries = util.list_entries()
            entries_up = [x.upper() for x in entries]
            if (q.upper() in entries_up):
                entry = util.get_entry(q)
                request.session["title"] = q
                request.session["entry"] = entry
                return render(request, "encyclopedia/md.html", {
                    "entry": markdown(entry),
                    "title": q,
                    "form": SForm()
                })
            else:
                sstring = []
                for entry in entries:
                    lentry = entry.lower()
                    if lentry.find(q.lower()) != -1:
                        sstring.append(entry)
                if len(sstring) == 0:
                    return render(request, "encyclopedia/err.html", {
                        "form": SForm(),
                        "message": err1
                    })
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
                    "message": err2,
                    "form": SForm()
                })
            else:
                util.save_entry(title, text)
                request.session["title"] = title
                request.session["entry"] = text
                return render(request, "encyclopedia/md.html", {
                    "form": SForm(),
                    "title": request.session["title"],
                    "entry": markdown(text)
                })
                return render(request, "encyclopedia/add.html",{
                    "form": SForm(),
                    "form2": NewForm()
                })
    else:
        return render(request, "encyclopedia/add.html", {
            "form": SForm(),
            "form2": NewForm (initial={"text": "# Title\n\nContent"})
        })

def edit(request):
    data = {"title": request.session["title"],
            "text": request.session["entry"]
            }
    f = NewForm(data)
    return render(request, "encyclopedia/edit.html", {
        "form": SForm(),
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
        "title": title,
        "form": SForm()
    })

def markdown(value):
    return md.markdown(value)



