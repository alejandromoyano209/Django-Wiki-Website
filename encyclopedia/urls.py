from django.urls import path

from . import views


app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
	path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("editpage/<str:entry>", views.editpage, name="editpage"),
    path("randompage", views.randompage, name="randompage"),
    path("<str:entry>", views.entrypage, name="entrypage")
]
