from PyQt5.QtWidgets import ( QWidget, QLineEdit, QTextEdit, QLabel,
        QRadioButton, QCheckBox, QPushButton, QHBoxLayout, QVBoxLayout,
        QFileDialog )

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

from functools import partial

from util import *
from icons import Icons



class ImageButton( QWidget ):
    def __init__( self, parent ):

        super().__init__()
        self.parent = parent
        self.index = -1
        self.path = "(None selected)"
        self.init_UI()


    def init_UI( self ):

        ##  Laziness
        get_icon = Icons().get_icon

        self.label = QLabel( self.path )
        self.pix = None
        self.iLabel = QLabel()

        self.btn = QPushButton( QIcon( get_icon( "document-open" ) ), "" )
        self.btn.clicked.connect( self.get_image )

        hbox = QHBoxLayout()
        hbox.addWidget( self.btn )
        hbox.addWidget( self.label, 1 )

        vbox = QVBoxLayout()
        vbox.addLayout( hbox )
        vbox.addWidget( self.iLabel )

        self.setLayout( vbox )


    def get_image( self ):

        path, ign = QFileDialog.getOpenFileName( self, "Choose image",
                get_data_dir() )

        if path != "":
            self.path = path
            self.label.setText( self.path )

            self.load_pix( self.path )
            self.parent.image_clicked( self.index, self.path )

    def load_pix( self, path ):

            self.pix = QPixmap( path )
            p = self.pix.scaledToHeight(WINDOW_HEIGHT/2,Qt.SmoothTransformation)
            self.iLabel.setPixmap( p )

    def get_width( self ):
        return( self.iLabel.pixmap().width() )

    def get_height( self ):
        return( self.iLabel.pixmap().height() )

    def reload( self, path ):

        self.path = path
        self.label.setText( path )
        self.load_pix( self.path )

    def clear( self ):
        self.path = "(None selected)"
        self.pix = None
        self.label.clear()
        self.iLabel.clear()



class RadioWidget( QWidget ):
    def __init__( self, parent, choices ):
        super().__init__()

        self.parent = parent

        self.index = -1

        self.choices = choices
        self.buttons = []

        self.value = "None"

        self.init_UI()


    def connect_all( self ):
        for btn in self.buttons:
            val = btn.text()
            btn.clicked.connect(
                    partial( self.parent.radio_clicked, self.index, val ))


    def disconnect_all( self ):

        for btn in self.buttons:
            btn.clicked.disconnect()


    def init_UI( self ):

        for c in self.choices:
            btn = QRadioButton( c )
            self.buttons.append( btn )

        ##  Set a default value
        if len( self.buttons ) > 0:
            self.buttons[ 0 ].setChecked( True )

        self.connect_all()

        hbox = QHBoxLayout()
        for btn in self.buttons:
            hbox.addWidget( btn )



        hbox.addWidget( QWidget(), 1 )

        self.setLayout( hbox )

    def set_checked( self, val ):
        for btn in self.buttons:
            if btn.text().lower() == val.lower():
                btn.setChecked( True )

    def clear_buttons( self ):
        if len( self.buttons ) > 0:
            self.buttons[ 0 ].setChecked( True )

        if len( self.buttons ) > 1:
            for btn in self.buttons[0:]:
                btn.setChecked( False )








class Tab( QWidget ):
    def __init__( self, parent, index, tab ):
        super().__init__()

        self.parent = parent
        self.index = index
        self.tab = tab

        self.widgets = []

        self.init_UI()


    def connect_all( self ):
        for widget in self.widgets:
            if type( widget ) == QLineEdit or type( widget ) == QTextEdit:
                widget.textChanged.connect(
                        partial( self.changed_field_value,
                            self.widgets.index( widget )))

            elif type( widget ) == RadioWidget:
                widget.connect_all()



    def disconnect_all( self ):
        for widget in self.widgets:
            if type( widget ) == QLineEdit or type( widget ) == QTextEdit:
                widget.textChanged.disconnect()
            elif type( widget ) == RadioWidget:
                widget.disconnect_all()

    def init_UI( self ):

        rows = []
        for row in self.tab.iter( "row" ):
            rows.append( self.parse_row( row ) )

        #for field in self.tab.iter( "field" ):
        #    layouts.append( self.parse_field( field ) )


        self.connect_all()

        vbox = group_hbox( rows )
        self.setLayout( vbox )




    def parse_row( self, row ):
        layouts = []
        for field in row.iter( "field" ):
            layouts.append( self.parse_field( field ))


        hbox = group_vbox( layouts )
        return( hbox )

            

    def parse_field( self, field ):

        name = ( field.find( "name" ).text ).strip()
        wType = ( field.find( "type" ).text ).strip()
        align = ( field.find( "align" ).text ).strip()

        ##  Type
        choices = []
        for choice in field.findall( "choice" ):
            choices.append( choice.text )

        widget = self.get_widget_by_type( wType.lower(), choices )
        if type( widget ) == RadioWidget or type( widget ) == ImageButton:
            widget.index = len( self.widgets )

        ##  Set the tooltip
        tip = field.find( "tip" )
        if tip != None:
            widget.setToolTip( tip.text )

        self.widgets.append( widget )

        ##  Horizontal
        if align[ 0 ].lower() == 'h':
            return( make_hbox( name, widget ))
        ##  Vertical
        else:
            return( make_vbox( name, widget ))


    def changed_field_value( self, index ):

        char = self.parent.characters[ self.parent.charIndex ]
        tab = char.tabs[ self.index ]
        widget = self.widgets[ index ]

        if type( widget ) == QLineEdit:
            tab.fields[ index ][ "value" ] = self.widgets[ index ].text()
        elif type( widget ) == QTextEdit:
            tab.fields[ index ][ "value" ] = self.widgets[ index ].toPlainText()


    def load_values( self, char ):

        idx = 0
        tab = char.tabs[ self.index ]
        for field in tab.fields:
            widget = self.widgets[ idx ]

            if type( widget ) == QLineEdit or type( widget ) == QTextEdit:
                if field[ "value" ] == "":
                    widget.clear()
                else:
                    widget.setText( field[ "value" ] )

            elif type( widget ) == RadioWidget:
                widget.set_checked( field[ "value" ] )

            elif type( widget ) == ImageButton:
                widget.reload( field[ "value" ] )
                field[ "width" ] = widget.get_width()
                field[ "height" ] = widget.get_height()

            idx += 1



    def clear_values( self ):

        for w in self.widgets:
            if type( w ) == QLineEdit or type( w ) == QTextEdit:
                w.clear()
            elif type( w ) == RadioWidget:
                w.clear_buttons()
            elif type( w ) == ImageButton:
                w.clear()


    def get_widget_by_type( self, wType, choices = None ):

        if wType == "short":
            return( QLineEdit() )

        elif wType == "long":
            return( QTextEdit() )

        elif wType == "radio" or wType == "choice":
            return( RadioWidget( self, choices ) )

        elif wType == "image" or wType == "img":
            return( ImageButton( self ))

    def radio_clicked( self, index, val ):
        char = self.parent.characters[ self.parent.charIndex ]
        tab = char.tabs[ self.index ]
        widget = self.widgets[ index ]

        #char = self.parent.characters[ self.parent.charIndex ]
        #tab = char.tabs[ self.index ]

        tab.fields[ index ][ "value" ] = val

    def image_clicked( self, index, val ):
        char = self.parent.characters[ self.parent.charIndex ]
        tab = char.tabs[ self.index ]
        widget = self.widgets[ index ]

        tab.fields[ index ][ "value" ] = val
        tab.fields[ index ][ "width" ] = widget.get_width()
        tab.fields[ index ][ "height" ] = widget.get_height()



def make_vbox( string, edit ):

    vbox = QVBoxLayout()

    label = QLabel( string )
    label.setToolTip( edit.toolTip() )
    vbox.addWidget( label )

    vbox.addWidget( edit )
    vbox.addWidget( QWidget(), 1 )

    return( vbox )


def make_hbox( string, edit ):
    hbox = QHBoxLayout()

    label = QLabel( string )
    label.setToolTip( edit.toolTip() )
    hbox.addWidget( label )

    hbox.addWidget( edit )

    return( hbox )


def group_hbox( list_of_hbox ):

    vbox = QVBoxLayout()

    for hbox in list_of_hbox:
        vbox.addLayout( hbox )

    return( vbox )


def group_vbox( list_of_vbox ):

    hbox = QHBoxLayout()

    for vbox in list_of_vbox:
        hbox.addLayout( vbox )

    return( hbox )
