#!/usr/bin/env python3

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import ( SimpleDocTemplate, Paragraph, Spacer, Image,
        PageBreak )
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from charInfo import CharacterInfo
from util import *


##  Fonts
fTitle = ( "Helvetica", 36 )
fSubTitle = ( "Helvetica", 28 )
fHeader = ( "Helvetica", 24 )
fName = ( "Helvetica", 18 )
fValue = ( "Helvetica", 14 )



def make_pdf( path, char ):


    fileName = "%s/%s.pdf" % ( path, char.listName )

    doc = SimpleDocTemplate( fileName, pagesize=letter,
            rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18 )

    story = []

    make_title_page( char, story )


    for tab in char.tabs:

        ##  Skip the page if all the values are blank
        numVal = get_number_of_values( tab )
        if numVal > 0:
            make_tab( tab, story )

    doc.build( story )



def make_title_page( char, story ):
    
    styles = getSampleStyleSheet()
    styles.add( ParagraphStyle( name = "Center", alignment = TA_CENTER ))

    pt = "<font size=%s>%s</font>" % ( fTitle[1], "Character Profile" )

    story.append( Paragraph( pt, styles[ "Center" ] ))
    story.append( Spacer( 1, 48 ))

    pt = "<font size=%s>%s</font>" % ( fSubTitle[1], char.listName )
    story.append( Paragraph( pt, styles[ "Center" ] ))


def make_tab( tab, story ):
    styles = getSampleStyleSheet()
    styles.add( ParagraphStyle( name = "Center", alignment = TA_CENTER ))

    story.append( PageBreak() )

    pt = "<font size=%s>%s</font>" % ( fHeader[1], tab.title )
    story.append( Paragraph( pt, styles[ "Center" ]) )
    story.append( Spacer( 1, 48 ))

    for field in tab.fields:

        ##  Skip the field if it doesn't have a value
        if field[ "value" ] != None and field[ "value" ] != "":

            pt = "<font size=%s>%s</font><br/>" % ( fName[1], field[ "name" ] )
            story.append( Paragraph( pt, styles[ "Normal" ]) )
            story.append( Spacer( 1, 16 ))

            pt = "<font size=%s>%s</font><br/>" % ( fValue[1], field[ "value" ])
            story.append( Paragraph( pt, styles[ "Normal" ]) )
            story.append( Spacer( 1, 30 ))


def get_number_of_values( tab ):

    num = 0
    for field in tab.fields:
        if field[ "value" ] != None and field[ "value" ] != "":
            num += 1

    return( num )


if __name__ == "__main__":
    main()
