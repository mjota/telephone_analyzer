#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import re
import gtk
import to_pdf


class main:

    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file("mainView.ui")

        links = {"on_window1_destroy": self.QuitAll,
        "on_button_start_clicked": self.LaunchCreate,
        "on_filechooserbutton1_file_set": self.OpenFile,
        "on_entry1_insert_text": self.LaunchMessage}

        builder.connect_signals(links)

        self.filefilter = builder.get_object("filefilter")
        self.filechooser = builder.get_object("filechooserbutton1")
        self.statusbar = builder.get_object("statusbar1")
        self.entrytext = builder.get_object("entry1")
        self.filefolder = builder.get_object("filechooserbutton2")

        self.context_id = self.statusbar.get_context_id("A")
        self.statusbar.push(self.context_id, "Selecciona fichero origen .cdr")

        self.filefilter.add_pattern("*.cdr")
        self.Tels = {}
        self.selectedfile = 0

    def LaunchCreate(self, widget):
        if self.selectedfile:
            if self.entrytext.get_text_length():
                self.ShowMessage("Generando ficheros...")
                self.MineryFiles()
            else:
                self.ShowMessage("Nombre de fichero final no seleccionado")
        else:
            self.ShowMessage("Debe seleccionar un fichero .cdr origen")

    def OpenFile(self, widget):
        fileName = self.filechooser.get_filename()
        try:
            fileR = open(fileName, "r")
        except IOError:
            self.ShowMessage("Imposible abrir fichero")
        except:
            self.ShowMessage("Imposible abrir fichero")
        else:
            self.fileC = csv.reader(fileR, delimiter=',')
            self.selectedfile = 1
            self.AnalyzeFile()

    def AnalyzeFile(self):
        #print "ORIGEN ,DATA, DESTINO , SEGUNDOS, PRECIO CARRIER,
        #PRECIO CLIENTE,NÚMERO MARCADO, TIEMPO GRATIS CARRIER"
        for row in self.fileC:
            if row[9] in self.Tels:
                self.Tels[row[9]].append([row[19].strip("\'"),
                row[0].strip("\'"), float(row[28].strip("\'")),
                float(row[33].strip("\'"))])
            else:
                self.Tels[row[9]] = [[row[19].strip("\'"), row[0].strip("\'"),
                 float(row[28].strip("\'")), float(row[33].strip("\'"))]]

        self.ShowMessage("Introduce nombre ficheros destino")

    def MineryFiles(self):
        for tel in self.Tels:
            typ = ""
            dwrite = []
            mins = {'nac': 0.0, 'int': 0.0, 'mov': 0.0, 'esp': 0.0}
            cost = {'nac': 0.0, 'int': 0.0, 'mov': 0.0, 'esp': 0.0}
            num = {'nac': 0, 'int': 0, 'mov': 0, 'esp': 0}
            total = {'num': 0, 'min': 0, 'cost': 0}
            #Número, data, minutos, tipo, coste
            for row in self.Tels[tel]:
                if len(row[0]) < 11:
                    typ = "Especial"
                    mins['esp'] += row[2]
                    cost['esp'] += row[3]
                    num['esp'] += 1
                elif re.match("34", row[0]):
                    if re.match("34(8|9)0", row[0]):
                        typ = "Especial"
                        mins['esp'] += row[2]
                        cost['esp'] += row[3]
                        num['esp'] += 1
                    elif re.match("34(6|7)", row[0]):
                        typ = "Movil"
                        mins['mov'] += row[2]
                        cost['mov'] += row[3]
                        num['mov'] += 1
                    else:
                        typ = "Nacional"
                        mins['nac'] += row[2]
                        cost['nac'] += row[3]
                        num['nac'] += 1
                else:
                    typ = "Internacional"
                    mins['int'] += row[2]
                    cost['int'] += row[3]
                    num['int'] += 1

                total['num'] += 1
                total['min'] += row[2]
                total['cost'] += row[3]
                dwrite.append([row[0], row[1], row[2], typ, row[3]])

            pdf = to_pdf.PDF(tel, self.filefolder.get_filename(),
            self.entrytext.get_text())
            pdf.GenerateFile(dwrite, num, mins, cost,
                 total, tel.strip("\'").lstrip("34"))

        self.ShowMessage("Ficheros creados correctamente")

    def GenerateFile(self, tel, num, mins, cost, total, ntel):

        pdf = to_pdf.PDF(ntel)
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 13)
        pdf.ln(20)
        pdf.cell(40)
        pdf.cell(0, 10, 'Resumen consumo', 0, 1)
        pdf.cell(40)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(50, 10, 'Tipo', 1, 0)
        pdf.cell(30, 10, 'N. Llam', 1, 0)
        pdf.cell(30, 10, 'Duracion', 1, 0)
        pdf.cell(30, 10, 'Coste', 1, 1)

        #Aquí for
        pdf.cell(40)
        pdf.set_font('Arial', '', 12)
        pdf.cell(50, 10, 'Nacional', 0, 0)
        pdf.cell(30, 10, str(num['nac']), 0, 0)
        pdf.cell(30, 10, str(mins['nac']), 0, 0)
        pdf.cell(30, 10, str(cost['nac']), 0, 1)

        pdf.cell(40)
        pdf.cell(50, 10, 'Movil', 0, 0)
        pdf.cell(30, 10, str(num['mov']), 0, 0)
        pdf.cell(30, 10, str(mins['mov']), 0, 0)
        pdf.cell(30, 10, str(cost['mov']), 0, 1)

        pdf.cell(40)
        pdf.cell(50, 10, 'Internacional', 0, 0)
        pdf.cell(30, 10, str(num['int']), 0, 0)
        pdf.cell(30, 10, str(mins['int']), 0, 0)
        pdf.cell(30, 10, str(cost['int']), 0, 1)

        pdf.cell(40)
        pdf.cell(50, 10, 'Especial', 0, 0)
        pdf.cell(30, 10, str(num['esp']), 0, 0)
        pdf.cell(30, 10, str(mins['esp']), 0, 0)
        pdf.cell(30, 10, str(cost['esp']), 0, 1)

        pdf.cell(40)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(50, 10, 'Total', 0, 0)
        pdf.cell(30, 10, str(total['num']), 0, 0)
        pdf.cell(30, 10, str(total['min']), 0, 0)
        pdf.cell(30, 10, str(total['cost']), 0, 1)

        pdf.add_page()
        pdf.set_font('Arial', 'B', 13)
        pdf.cell(5)
        #Telefono, Descripción, Fecha, Duración, T, Importe
        pdf.cell(0, 10, 'Listado llamadas', 0, 1)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(5)
        pdf.cell(40, 6, 'Telefono', 1, 0)
        pdf.cell(40, 6, 'Fecha', 1, 0)
        pdf.cell(30, 6, 'Duracion', 1, 0)
        pdf.cell(30, 6, 'Tipo', 1, 0)
        pdf.cell(30, 6, 'Importe', 1, 1)

        pdf.set_font('Arial', '', 10)

        for row in tel:
            pdf.cell(5)
            pdf.cell(40, 6, row[0], 1, 0)
            pdf.cell(40, 6, row[1], 1, 0)
            pdf.cell(30, 6, str(row[2]), 1, 0)
            pdf.cell(30, 6, row[3], 1, 0)
            pdf.cell(30, 6, str(row[4]), 1, 1)

        pdf.output(self.filefolder.get_filename() + "/" +
        self.entrytext.get_text() + " - " + ntel + '.pdf', 'F')

    def LaunchMessage(self, *widget):
        self.ShowMessage("Selecciona \"Generar Ficheros\" para finalizar")

    def ShowMessage(self, message):
        self.statusbar.pop(self.context_id)
        self.statusbar.push(self.context_id, message)

    def QuitAll(self, widget):
        gtk.main_quit()


if __name__ == '__main__':
    main()
    gtk.main()
