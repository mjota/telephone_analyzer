#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import pygtk
import gtk
import gobject


class main:

    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file("mainView.ui")

        links = {"on_window1_destroy": self.QuitAll,
        "on_button_start_clicked": self.LaunchCreate,
        "on_filechooserbutton1_file_set": self.OpenFile,
        "on_entry1_insert_text": self.LaunchMessage,
        "on_button_refresh_clicked": self.Refresh}

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
                self.ShowMessage("Generando ficheros")
                self.GenerateFiles()
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
        #print "ORIGEN , DESTINO , SEGUNDOS, PRECIO CARRIER, PRECIO CLIENTE,NÚMERO MARCADO, TIEMPO GRATIS CARRIER"
        for row in self.fileC:
            if row[9] in self.Tels:
                self.Tels[row[9]].append([row[19].strip("\'"), float(row[28].strip("\'")), float(row[33].strip("\'"))])
            else:
                self.Tels[row[9]] = [[row[19].strip("\'"), row[28].strip("\'"), row[33].strip("\'")]]

        self.ShowMessage("Introduce nombre ficheros destino")

    def GenerateFiles(self):
        print self.filefolder.get_filename()
        print self.entrytext.get_text()
        print self.filechooser.get_filename()

    def Refresh(self, widget):
        self.Tels = {}
        self.selectedfile = 0
        self.entrytext.set_text("")
        self.filechooser.set_current_folder("")
        self.ShowMessage("Selecciona fichero origen .cdr")

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
