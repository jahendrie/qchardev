#!/usr/bin/env python3
#===============================================================================
#   qCharDev    |   version 0.90    |   GPL v3      |   2018-05-03
#   James Hendrie                   |   hendrie.james@gmail.com
#
#   PyQt5 character developer
#
#   ---------------------------------------------------------------------------
#
#    Copyright (C) 2017, 2018 James Hendrie
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#===============================================================================

import sys, os
from PyQt5.QtWidgets import QApplication
from mainWindow import MainWindow

from PyQt5.QtGui import QIcon
from icons import Icons


def print_help():
    #print_usage()
    print( "qCharDev is a program that will, at least ostensibly, make for" )
    print( "easier development of character profiles for any fiction you" )
    print("happen to be writing.\n" )
    print("The questions are kept in an XML template file (data/template.xml),")
    print( "so have a peek at that if you wish to add your own, or replace it" )
    print("altogether.  If you misplace the file (silly you!), there is no need")
    print( "to fret if you've already saved your characters.  A copy of the" )
    print("template used is kept in the .sav file, and loaded whenever you load")
    print( "your characters." )


def main():

    urls = []
    if len( sys.argv ) > 1:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print_help()
            return( 0 )


    app = QApplication( sys.argv )

    app.setWindowIcon( Icons().get_icon( "application-icon" ))

    win = MainWindow()

    sys.exit( app.exec_() )


if __name__ == "__main__":
    main()
