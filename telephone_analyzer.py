#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys


class main:

    def __init__(self):
        self.Tels = {}
        self.OpenFile()
        self.AnalyzeFile()

    def OpenFile(self):
        try:
            fileR = open(sys.argv[1], "r")
        except IOError:
            print "\nNombre del fichero no válido \n"
        except:
            print "\nDebe introducir el nombre del fichero \n"

        self.fileC = csv.reader(fileR, delimiter=',')

    def AnalyzeFile(self):
        print "ORIGEN , DESTINO , SEGUNDOS, PRECIO CARRIER, PRECIO CLIENTE,NÚMERO MARCADO, TIEMPO GRATIS CARRIER"
        for row in self.fileC:
            if row[9] in self.Tels:
                self.Tels[row[9]].append([row[19].strip("\'"), float(row[28].strip("\'")), float(row[33].strip("\'"))])
            else:
                self.Tels[row[9]] = [[row[19].strip("\'"), row[28].strip("\'"), row[33].strip("\'")]]

        #print Tels

        for row in self.Tels:
            print row
            print self.Tels[row][0][0]
            print self.Tels[row][1][0]


if __name__ == '__main__':
    main()
