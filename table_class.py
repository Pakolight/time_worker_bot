
from create_table_fpdf2 import PDF
from loguru import logger
from row_method import Table_data
table = Table_data()

data2 = [
    ["Date", "Project", "Tasks", "Time start", "Time end", "Duration", "Descreption", "Km", "Km cost", "Other", "Total","Price"],
    ["Jules", "Smith", "34", "San Juan","5",'6','7','8','9','10','11','12'],
]

print(type(data2))

table.creat()

data = table.out()



pdf = PDF('L')
pdf.add_page()
pdf.set_font("Times", size=10)

pdf.create_table(table_data = data,title='Time list', cell_width='even')
pdf.ln()


pdf.output('Timelist.pdf')


data2 = [
    ["Date", "Project", "Tasks", "Time start", "Time end", "Duration", "Descreption", "Km", "Km cost", "Other", "Total","Price"],
    ["Jules", "Smith", "34", "San Juan","5",'6','7','8','9','10','11','12'],
]

print(data2)
