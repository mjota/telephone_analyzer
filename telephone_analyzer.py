#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import re
import gtk
import to_pdf


class main:

    COST_MIN = 2.07    # Coste minuto nacional. EN CÉNTIMOS

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
        self.window = builder.get_object("window1")

        self.window.set_icon_from_file("logo_pb.png")
        statusIcon = gtk.StatusIcon()
        statusIcon.set_from_file("logo_pb.png")
        statusIcon.set_visible(True)

        self.context_id = self.statusbar.get_context_id("A")
        self.statusbar.push(self.context_id, "Selecciona fichero origen .cdr")

        self.filefilter.add_pattern("*.cdr")
        self.Tels = {}
        self.selectedfile = 0

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
                row[0].strip("\'"), int(float(row[28].strip("\'")) + 0.99),
                float(row[33].strip("\'"))])
            else:
                self.Tels[row[9]] = [[row[19].strip("\'"), row[0].strip("\'"),
                 int(float(row[28].strip("\'")) + 0.99),
                 float(row[33].strip("\'"))]]

        self.ShowMessage("Introduce nombre ficheros destino")

    def LaunchCreate(self, widget):
        if self.selectedfile:
            if self.entrytext.get_text_length():
                self.ShowMessage("Generando ficheros...")
                self.MineryFiles()
            else:
                self.ShowMessage("Nombre de fichero final no seleccionado")
        else:
            self.ShowMessage("Debe seleccionar un fichero .cdr origen")

    def MineryFiles(self):
        for tel in self.Tels:
            typ = ""
            dwrite = []
            mins = {'nac': 0, 'int': 0, 'mov': 0, 'esp': 0}
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

            pdf = to_pdf.PDF(tel.strip("\'").lstrip("34"),
            self.filefolder.get_filename(), self.entrytext.get_text())

            pdf.GenerateFile(dwrite, num, mins, cost, total)
            self.writeCSV(total, tel.strip("\'").lstrip("34"))

        self.ShowMessage("Ficheros creados correctamente")
        self.Tels = {}
        self.selectedfile = 0

    def writeCSV(self, total, tel):
        """Create CSV file"""
        fileW = open(self.filefolder.get_filename() + "/" +
        self.entrytext.get_text() + ".csv", "a")
        fileC = csv.writer(fileW)
        fileC.writerow([tel, total['num'], str(total['min']),
        str(total['cost'])])
        fileW.close()

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
