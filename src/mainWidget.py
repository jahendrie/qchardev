import os

##  PyQt5 Stuff
from PyQt5.QtWidgets import ( QWidget, QVBoxLayout, QHBoxLayout, QFileDialog,
        QTabWidget, QListWidget, QListWidgetItem, QPushButton, QSplitter )

from PyQt5.QtGui import QIcon
from PyQt5.Qt import QApplication
from PyQt5.QtCore import Qt

##  Other stuff
import sip
import subprocess
import xml.etree.ElementTree as ET

##  My stuff
from icons import Icons
from util import *

from charInfo import CharacterInfo

from tabs import Tab
#from tabBasics import TabBasics
#from tabPhysical import TabPhysical
#from tabIntellectual import TabIntellectual
#from tabPersonality import TabPersonality


class MyListWidget( QListWidget ):

    def __init__( self, parent = None ):
        super().__init__()
        self.parent = parent


        self.init_UI()

    def init_UI( self ):
        ##  The list, on the left-hand side, with buttons at the bottom
        listButtons = QHBoxLayout()
        listButtons.addWidget( self.parent.addChar )
        listButtons.addWidget( self.parent.removeChar )
        listButtons.addWidget( QWidget(), 1 )

        listLayout = QVBoxLayout()
        listLayout.addWidget( self.parent.listWidget )
        listLayout.addLayout( listButtons )

        self.setLayout( listLayout )





class MainWidget( QWidget ):

    def __init__( self, parent = None ):

        super().__init__()
        self.parent = parent

        self.template = None
        self.characters = []
        self.charIndex = 0

        self.init_UI()



    def connect_all( self ):

        self.addChar.clicked.connect( self.add_character )
        self.removeChar.clicked.connect( self.remove_character )

        self.listWidget.currentItemChanged.connect( self.item_changed )
        self.listWidget.itemChanged.connect( self.item_text_changed )

        for r in range( self.tabs.count() ):
            w = self.tabs.widget( r )
            w.connect_all()

    
    def disconnect_all( self ):
        self.addChar.clicked.disconnect()
        self.removeChar.clicked.disconnect()

        self.listWidget.currentItemChanged.disconnect()
        self.listWidget.itemChanged.disconnect()

        for r in range( self.tabs.count() ):
            w = self.tabs.widget( r )
            w.disconnect_all()



    def disable_stuff( self, disabled ):

        self.addChar.setDisabled( disabled )
        self.removeChar.setDisabled( disabled )




    def init_UI( self ):

        ##  Just to make life easier
        get_icon = Icons().get_icon

        ##  List of characters
        self.listWidget = QListWidget( self )

        ##  Add character button
        self.addChar = QPushButton( QIcon( get_icon( "list-add")), "" )
        self.addChar.setToolTip( "Add a character" )

        ##  Remove character button
        self.removeChar = QPushButton( QIcon( get_icon( "list-remove")), "" )
        self.removeChar.setToolTip( "Remove selected character" )

        ##  Bullshit to make qsplitter work
        self.list = MyListWidget( self )


        ##  Initial template
        self.template = self.parent.get_template()

        ##  Tab widget
        self.tabs = QTabWidget()

        self.load_tabs()


        ##  Tabs start out disabled
        self.tabs.setDisabled( True )


        ##  Connect it up
        self.connect_all()


        ##============= LAYOUTS


        splitter = QSplitter()
        splitter.addWidget( self.list )
        splitter.addWidget( self.tabs )

        splitter.setSizes( [ (WINDOW_WIDTH * .25), (WINDOW_WIDTH * .75) ] )

        ##  Set the layout
        hbox = QHBoxLayout()
        hbox.addWidget( splitter )
        self.setLayout( hbox )



    def load_tabs( self ):
        if self.template != None:
            tabIndex = 0
            for tab in self.template.iter( "tab" ):
                widget = Tab( self, tabIndex, tab )
                tabIndex += 1
                self.tabs.addTab( widget, tab.find( "title" ).text )


    def add_character( self ):

        char = CharacterInfo( self.template )
        self.characters.append( char )

        li = QListWidgetItem( char.listName )
        li.setFlags( li.flags() | Qt.ItemIsEditable )
        self.listWidget.addItem( li )
        self.listWidget.setCurrentItem( li )

        ##  Enable the tabs widget
        self.tabs.setDisabled( False )



    def remove_character( self ):

        idx = self.listWidget.currentRow()
        li = self.listWidget.item( idx )
        if li != None:
            ##  Kill whatever character at the index
            null = self.characters.pop( idx )

            ni = self.listWidget.item( idx + 1 )
            pi = self.listWidget.item( idx - 1 )

            #self.listWidget.currentItemChanged.disconnect()

            self.disconnect_all()

            sip.delete( li )

            self.listWidget.currentItemChanged.connect( self.item_changed )
            if ni != None:
                self.listWidget.setCurrentItem( ni )
                idx = self.listWidget.currentRow()
                self.charIndex = idx
                self.load_values( self.characters[ idx ] )
            elif pi != None:
                self.listWidget.setCurrentItem( pi )
                idx = self.listWidget.currentRow()
                self.charIndex = idx
                self.load_values( self.characters[ idx ] )
            else:
                self.charIndex = -1
                self.tabs.setDisabled( True )
                self.listWidget.currentItemChanged.connect( self.item_changed )
                self.clear_values()


            self.connect_all()



    def item_changed( self ):

        li = self.listWidget.currentItem()
        if li != None:
            self.charIndex = self.listWidget.currentRow()
            self.load_values( self.characters[ self.charIndex ] )

    def item_text_changed( self ):

        li = self.listWidget.currentItem()
        if li != None:
            self.characters[ self.charIndex ].listName = li.text()


    def load_values( self, char ):

        for t in range( len (self.characters[ self.charIndex ].tabs )):
            tab = self.tabs.widget( t )
            tab.load_values( char )


    def clear_values( self ):
        for t in range( self.tabs.count() ):
            w = self.tabs.widget( t )
            w.clear_values()
        #if len( self.characters ) > 0:
        #    for t in range( len(self.characters[ self.charIndex ].tabs )):
        #        tab = self.tabs.widget( t )
        #        tab.clear_values()


    def clear_all( self ):

        ##  Kill characters and disable the tabs
        self.characters = []
        self.tabs.setDisabled( True )

        ##  Kill tabs
        self.tabs.clear()

        ##  Kill the list
        self.listWidget.clear()



    def load_list( self ):

        for char in self.characters:

            li = QListWidgetItem( char.listName )
            li.setFlags( li.flags() | Qt.ItemIsEditable )
            self.listWidget.addItem( li )


    def reload( self, template, characters ):
        self.disconnect_all()

        self.clear_all()
        self.template = template

        #c = characters[ 0 ]
        #print( c.tabs[ 0 ][0][ "name" ] )
        
        self.characters = characters
        self.load_list()
        self.load_tabs()

        self.connect_all()

        li = self.listWidget.item( 0 )
        if li != None:
            self.listWidget.setCurrentItem( li )
            self.tabs.setDisabled( False )
