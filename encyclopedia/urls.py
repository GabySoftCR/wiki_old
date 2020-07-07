from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>/", views.read_entry, name="read_entry"),
    path("s_sub", views.s_sub, name="s_sub"),
    path("add", views.add, name="add"),
    path("edit", views.edit, name="edit"),
    path("save", views.save, name="save"),
    path("rand", views.rand, name="rand"),
    path("markdown", views.markdown, name="markdown")
]
