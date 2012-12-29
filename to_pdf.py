#!/usr/bin/env python
# -*- coding: Windows-1252 -*-

from fpdf import FPDF


class PDF(FPDF):

    def __init__(self, tel, folder, filename):
        super(PDF, self).__init__()
        self.tel = tel
        self.folder = folder
        self.filename = filename

    def header(self):
        # Logo
        self.image('logo_pb.png', 10, 8, 45)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(100, 10, 'Registro telefónico - ' +
        self.tel, 0, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def GenerateFile(self, tel, num, mins, cost, total):
        """Non elegant form to create pdf"""
        self.alias_nb_pages()
        self.add_page()
        self.set_font('Arial', 'B', 13)
        self.ln(20)
        self.cell(40)
        self.cell(0, 10, 'Resumen consumo', 0, 1)
        self.cell(40)
        self.set_font('Arial', 'B', 12)
        self.cell(50, 10, 'Tipo', 1, 0)
        self.cell(30, 10, 'N. Llam', 1, 0)
        self.cell(30, 10, 'Duración', 1, 0)
        self.cell(30, 10, 'Coste', 1, 1)

        self.cell(40)
        self.set_font('Arial', '', 12)
        self.cell(50, 10, 'Nacional', 0, 0)
        self.cell(30, 10, str(num['nac']), 0, 0)
        self.cell(30, 10, str(mins['nac'] / 60).zfill(2)
        + ":" + str(mins['nac'] % 60).zfill(2), 0, 0)
        self.cell(30, 10, str("%.4f" % (cost['nac'] / 100)), 0, 1)

        self.cell(40)
        self.cell(50, 10, 'Móvil', 0, 0)
        self.cell(30, 10, str(num['mov']), 0, 0)
        self.cell(30, 10, str(mins['mov'] / 60).zfill(2)
        + ":" + str(mins['mov'] % 60).zfill(2), 0, 0)
        self.cell(30, 10, str("%.4f" % (cost['mov'] / 100)), 0, 1)

        self.cell(40)
        self.cell(50, 10, 'Internacional', 0, 0)
        self.cell(30, 10, str(num['int']), 0, 0)
        self.cell(30, 10, str(mins['int'] / 60).zfill(2)
        + ":" + str(mins['int'] % 60).zfill(2), 0, 0)
        self.cell(30, 10, str("%.4f" % (cost['int'] / 100)), 0, 1)

        self.cell(40)
        self.cell(50, 10, 'Especial', 0, 0)
        self.cell(30, 10, str(num['esp']), 0, 0)
        self.cell(30, 10, str(mins['esp'] / 60).zfill(2)
        + ":" + str(mins['esp'] % 60).zfill(2), 0, 0)
        self.cell(30, 10, str("%.4f" % (cost['esp'] / 100)), 0, 1)

        self.cell(40)
        self.set_font('Arial', 'B', 12)
        self.cell(50, 10, 'Total', 0, 0)
        self.cell(30, 10, str(total['num']), 0, 0)
        self.cell(30, 10, str(total['min'] / 60).zfill(2)
        + ":" + str(total['min'] % 60).zfill(2), 0, 0)
        self.cell(30, 10, str("%.2f" % (total['cost'] / 100)) + "€", 0, 1)

        self.add_page()
        self.set_font('Arial', 'B', 13)
        self.cell(5)
        self.cell(0, 10, 'Listado llamadas', 0, 1)
        self.set_font('Arial', 'B', 10)
        self.cell(5)
        self.cell(40, 6, 'Teléfono', 1, 0)
        self.cell(40, 6, 'Fecha', 1, 0)
        self.cell(30, 6, 'Duración', 1, 0)
        self.cell(30, 6, 'Tipo', 1, 0)
        self.cell(30, 6, 'Importe', 1, 1)

        self.set_font('Arial', '', 10)

        for row in tel:
            self.cell(5)
            self.cell(40, 6, row[0], 1, 0)
            self.cell(40, 6, row[1], 1, 0)
            self.cell(30, 6, str(row[2] / 60).zfill(2) + ":"
            + str(row[2] % 60).zfill(2), 1, 0)
            self.cell(30, 6, row[3], 1, 0)
            self.cell(30, 6, str(row[4] / 100).zfill(2), 1, 1)

        self.output(self.folder + "/" +
        self.filename + " - " + self.tel + '.pdf', 'F')
