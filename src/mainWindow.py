import os

from PyQt5.QtWidgets import (QMainWindow, QDesktopWidget, qApp, QMessageBox,
        QFileDialog )
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QAction

from mainWidget import MainWidget
#from aboutWidget import AboutWidget
from binFile import *

from util import *
from icons import Icons
from recents import Recents

import xml.etree.ElementTree as ET
from functools import partial

##  PDF export module stuff
canExportPDF = False
import importlib
rl = importlib.util.find_spec( "reportlab" )
if rl != None:
    from pdf_stuff import make_pdf
    canExportPDF = True


class MainWindow( QMainWindow ):

    #opts = read_config()
    urls = []

    def __init__( self ):
        super().__init__()

        self.path = ""
        self.template = None
        self.zTemplate = None

        self.recents = []

        self.init_UI()


    def init_UI( self ):
        self.mainWidget = MainWidget( self )

        self.statusBar()
        self.build_menu_bar()

        self.setCentralWidget( self.mainWidget )

        self.resize( WINDOW_WIDTH, WINDOW_HEIGHT )
        self.center_window()
        self.setWindowTitle( "qCharDev" )
        self.show()


    def center_window( self ):
        f = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        f.moveCenter( center )
        self.move( f.topLeft() )

    
    def build_menu_bar( self ):

        get_icon = Icons().get_icon

        ########  Actions

        ##  Save
        saveAction = QAction( QIcon( get_icon( "document-save-as" )),
                "&Save",self)
        saveAction.setShortcut( "Ctrl+S" )
        saveAction.setStatusTip( "Save file" )
        saveAction.triggered.connect( self.save_file )

        ##  Save As
        saveAsAction = QAction( QIcon( get_icon( "document-save" )),
                "&Save As",self)
        saveAsAction.setStatusTip( "Save file as..." )
        saveAsAction.triggered.connect( self.save_file_as )
        
        ##  Open
        openAction = QAction( QIcon( get_icon( "document-open")), "&Open", self)
        openAction.setShortcut( "Ctrl+O" )
        openAction.setStatusTip( "Open file" )
        openAction.triggered.connect( self.open_file )

        ##  Import template
        importAction = QAction( QIcon( get_icon( "document-open")),
                "&Import template", self )
        importAction.setStatusTip( "Import a template file" )
        importAction.triggered.connect( self.import_template )

        ##  Export
        exportAction = QAction( QIcon( get_icon( "document-save")), "&Export PDF",
                self )
        exportAction.setShortcut( "Ctrl+E" )
        exportAction.setStatusTip( "Export each character's profile as a PDF" )
        exportAction.triggered.connect( self.export_file )
        if not canExportPDF:
            exportAction.setDisabled( True )

        ##  Exit
        exitAction = QAction( QIcon( get_icon( "application-exit")),
                "&Exit", self )
        exitAction.setShortcut( "Ctrl+Q" )
        exitAction.setStatusTip( "Exit the application" )
        exitAction.triggered.connect( qApp.quit )



        ##  About action
        aboutAction = QAction( QIcon( get_icon( "help-about" )), "&About", self)
        aboutAction.setStatusTip( "Information about the program" )
        aboutAction.triggered.connect( self.about )


        ##  Create the menubar
        menuBar = self.menuBar()

        ##  Create file menu
        fileMenu = menuBar.addMenu( "&File" )
        fileMenu.addAction( openAction )

        ##  Recents menu
        self.recentsMenu = fileMenu.addMenu( "Recent" )

        fileMenu.addSeparator()
        fileMenu.addAction( saveAction )
        fileMenu.addAction( saveAsAction )
        fileMenu.addSeparator()
        fileMenu.addAction( exportAction )
        fileMenu.addSeparator()
        fileMenu.addAction( exitAction )

        ##  Create edit menu
        editMenu = menuBar.addMenu( "&Edit" )
        editMenu.addAction( importAction )

        helpMenu = menuBar.addMenu( "&Help" )
        helpMenu.addAction( aboutAction )


        self.load_recents_menu()



    def load_recents_menu( self ):
        self.recentsMenu.clear()
        recents = Recents().load_recents()


        if len( recents ) == 0:
            self.recentsMenu.setEnabled( False )

        else:
            recents.reverse()

            self.recentsMenu.setEnabled( True )

            for path in recents:
                rAction = QAction( os.path.basename( path ), self )
                rAction.setStatusTip( "Path:  %s" % path )
                rAction.triggered.connect( partial( self.load_file, path ))
                self.recentsMenu.addAction( rAction )


    def update_recents( self, path ):

        Recents().append_recent( path )
        self.load_recents_menu()



    def save_file_as( self ):

        path, ign = QFileDialog.getSaveFileName( self, "Save to file",
                get_data_dir(), "*.sav" )

        if path != "":

            if path[ -4 : ].lower() != '.sav':
                path += ".sav"

            self.path = path
            self.save_file()


    def save_file( self ):

        if self.path != "":
            save_file( self.path, self.zTemplate, self.mainWidget.characters )

            self.update_recents( self.path )
            self.statusBar().showMessage( "File saved", 2000 )
        else:
            self.save_file_as()


    def load_file( self, path ):

        self.path = path

        template, zTemplate, characters = load_file( path )

        self.template = template
        self.zTemplate = zTemplate

        self.mainWidget.reload( template, characters )

        self.update_recents( self.path )
        self.statusBar().showMessage( "File loaded", 2000 )


    def open_file( self ):
        path, ign = QFileDialog.getOpenFileName( self, "Open file",
                get_data_dir(), "*.sav" )

        if path != "":
            self.load_file( path )


    def export_file( self ):
        if canExportPDF and len( self.mainWidget.characters ) > 0:

            path = QFileDialog.getExistingDirectory( self,
                    "Export characters to...", export_path() )

            if path != "":
                for char in self.mainWidget.characters:
                    make_pdf( path, char )

                self.statusBar().showMessage(
                        "Character profiles exported", 2000 )
                
        elif len( self.mainWidget.characters ) == 0:
            QMessageBox.warning( self, "Hey dummy",
                    "You'll need characters before you can export their \
                            profiles.", QMessageBox.Ok )



    def about( self ):
        aboutStr = """
        qCharDev is a a PyQt application designed to help you
        develop characters for your fiction.

        Version:    %s
        License:    GPLv3 - https://www.gnu.org/licenses/gpl-3.0.txt
        Author:     James Hendrie - hendrie.james@gmail.com
        Git:           https://github.com/jahendrie/qytdl
        """ % VERSION
        msg = QMessageBox.about( self, "About qCharDev", aboutStr )


    
    def template_from_file( self, path ):
        try:
            fin = open( path, "r" )
            txt = fin.read()
            fin.close()

            self.template = ET.fromstring( txt )
            self.zTemplate = lzma.compress( bytes( txt, "utf-8"))

            return( self.template )

        except FileNotFoundError:
            raise FileNotFoundError


    def import_template( self ):
        ret = QMessageBox.warning( self, "Warning",
                "Importing a template will discard all unsaved character data.\
                Do you wish to continue?",
                QMessageBox.Yes, QMessageBox.No )


        if ret == QMessageBox.Yes:

            path, ign = QFileDialog.getOpenFileName( self, "Import template",
                    get_data_dir(), "*.xml" )

            if path != "":

                template = self.template_from_file( path )
                self.path = ""

                self.mainWidget.reload( template, [] )

        


    def get_template( self ):

        try:
            template = self.template_from_file( template_path() )
            
            return( template )

        except FileNotFoundError:
            if self.path == "":
                return( None )
            else:
                txt = get_template_from_save( self.path )

                self.template = ET.fromstring( txt )
                self.zTemplate = lzma.compress( bytes( txt, "utf-8"))

                return( self.template )
