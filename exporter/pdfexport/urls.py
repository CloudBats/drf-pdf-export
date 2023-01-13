from django.urls import path
from pdfexport import views

urlpatterns = [
    path("export/", views.RenderHTML.as_view()),
    path("templates/", views.TemplatesView.as_view())
]
