import jinja2
import pdfkit
import pathlib

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings


def get_template_env():
    """Establish the JINJA2 environment and where to search for the
    html templates."""
    template_loader = jinja2.FileSystemLoader(searchpath=settings.REPORTS_TEMPLATES)
    return jinja2.Environment(loader=template_loader)


class TemplatesView(APIView):

    def get(self, request):
        env = get_template_env()
        return Response(dict(msg="All templates from the env", tempalates=env.list_templates()))


class RenderHTML(APIView):

    @staticmethod
    def html2pdf(doc: str):
        """Using the html doc will render it to a pdf binary"""
        options = {
            'page-size': 'Letter',
            'margin-top': '0.35in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }

        pdf_obj = pdfkit.PDFKit(doc, 'string', verbose=True, options=options)

        return pdf_obj.to_pdf()

    @staticmethod
    def render_report_template(template_file: str, data: dict) -> str:
        """Renders a html page using jinja2"""
        template_env = get_template_env()
        template = template_env.get_template(template_file)
        output_text = template.render(
            name=data["name"],
            address=data["address"],
            date=data["date"],
            invoice=data["invoice"],
        )

        return output_text

    def get(self, request):
        doc_html = self.render_report_template("simple.html", dict(
            name="Vlad",
            address="Bucuresti",
            date="22/01/1996",
            invoice="AJ-7891"
        ))

        data = self.html2pdf(doc_html)
        response = HttpResponse(
            content=data,
            headers={'Content-Disposition': 'attachment'},
            content_type='application/pdf',
            status=status.HTTP_200_OK
        )

        return response

