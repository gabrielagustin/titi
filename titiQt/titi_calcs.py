#!/usr/bin/env python
# -*- encoding: utf8 -*-

#===============================================================================
# META
#===============================================================================

__version__ = "0.2.0"
__license__ = "GPL v3"
__author__ = "Emiliano López, Gabriel García"
__email__ = "emiliano dot lopezat gmail dot com, gabiagus gmail dot com"
__url__ = "https://github.com/emilopez/titi"
__date__ = "2014-09-10"

import sys
import titi_calcs_app

def main():
    app = titi_calcs_app.QtGui.QApplication(sys.argv)
    ventana = titi_calcs_app.CalcsApp()
    width = 900
    height = 600
    ventana.setFixedSize(width, height)
    ventana.show()
    sys.exit(app.exec_())

if __name__== '__main__':
    main()

