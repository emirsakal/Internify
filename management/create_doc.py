from docxtpl import DocxTemplate
from docx2pdf import convert
from django.conf import settings
import os
import pythoncom
import uuid

def create_letter(context, name):
	name += f'_{uuid.uuid4().hex}.pdf'
	
	# Read the Word document
	doc = DocxTemplate(str(settings.BASE_DIR) + '\\letter.docx')

	doc.render(context)

	# Save the updated Word document
	doc.save(str(settings.BASE_DIR) +'\\template.docx')

	# Convert the Word document to PDF
	pythoncom.CoInitializeEx(0)
	convert(str(settings.BASE_DIR) + "\\template.docx", str(settings.BASE_DIR) + '\\uploads\\files\\' + name)

	# Remove the Word document
	os.remove(str(settings.BASE_DIR) + "\\template.docx")
	
	return name