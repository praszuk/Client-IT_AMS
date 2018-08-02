from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import RGBColor
from docx.oxml.shared import OxmlElement, qn


hardware = ['jakas nazwa', 'jakis opis', 'jakis SN1']

client = 'Jan Kowalski'
middleman = 'Grazyna Nowak'
date_start = '25 lipca 2018'
date_end = '1 sierpnia 2018'

lender_address = 'Cisco Systems\nul. Domaniewska 39 B\n02-627, Warszawa\nPoland'

document = Document('template.docx')

for i in range(10):
    cells = document.tables[0].add_row().cells
    cells[0].text = hardware[0] + '{}'.format(i)
    cells[1].text = hardware[1] + '{}'.format(i)
    cells[2].text = hardware[2] + '{}'.format(i)


for r in document.tables[1].rows:
    for cell in r.cells:
        if '<client>' in cell.text:
            cell.text = cell.text.replace('<client>', client)
        elif '<middleman>' in cell.text:
            cell.text = cell.text.replace('<middleman>', middleman)
            cell.paragraphs[0].paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

for idx, p in enumerate(document.paragraphs):
        if '<date_start>' in p.text:
            p.text = ''
            p.add_run('Dnia ')
            p.add_run(date_start).bold = True
            p.add_run(' r. dokonano wypożyczenia sprzętu o następujących parametrach:')

        elif '<date_end>' in p.text:
            p.text = ''
            p.add_run('Okres wypożyczenia do dnia:').underline = True
            p.add_run(' ')

            p_date = p.add_run(date_end)
            p_date.bold = True
            color = RGBColor(0xff, 0x00, 0x00)  # RED
            p_date.font.color.rgb = color

        elif '<client_info>' in p.text:
            p.text = lender_address

document.save('demo_modified.docx')



