from create_table_fpdf2 import PDF

class Add:
    data = [
        ["Date", "Project", "Tasks", "Time start", "Time end", "Duration", "Descreption", "Km", "Km cost", "Other",
         "Total", "Price"],
    ]

    def add_list(self):
        add_args = None







data = [
    ["Date", "Project", "Tasks", "Time start", "Time end", "Duration", "Descreption", "Km", "Km cost", "Other", "Total","Price"],
    ["Jules", "Smith", "34", "San Juan","5",'6','7','8','9','10','11','12'],
]


pdf = PDF('L')
pdf.add_page()
pdf.set_font("Times", size=10)

pdf.create_table(table_data = data,title='Time list', cell_width='even')
pdf.ln()


pdf.output('Timelist.pdf')

