from io import BytesIO
import os
from django.conf import settings

#A stream implementation using an in-memory bytes buffer
                       # It inherits BufferIOBase

from django.http import HttpResponse
from django.template.loader import get_template

#pisa is a html2pdf converter using the ReportLab Toolkit,
#the HTML5lib and pyPdf.
from django.conf import settings
import os

from xhtml2pdf import pisa
#difine render_to_pdf() function

# funksjon som tar inn hvilke template som skal rendres til pdf sammen med context dictionaryen for innholdet i denne
# sender så en HttpResponse som rendrer innhold om til pdf basert på templaten.
def render_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()

     #This part will create the pdf.
     pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), dest=result, link_callback=fetch_resources )
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None

# gjør det mulig å ta inn bilder i pdf-en

def fetch_resources(uri, rel):
  path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
  return path
