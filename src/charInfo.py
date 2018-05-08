
class CharacterInfoTab():

    def __init__( self ):
        self.title = "Null title"
        self.fields = []


class CharacterInfo( ):

    def __init__( self, template ):

        ##  Basics
        self.listName = "New Character"

        self.tabs = []

        if template != None:
            for tab in template.iter( "tab" ):

                #fields = []
                t = CharacterInfoTab()
                t.title = tab.find( "title" ).text

                for field in tab.iter( "field" ):
                    d = {}
                    d[ "name" ] = field.find( "name" )
                    d[ "type" ] = field.find( "type" )
                    d[ "align" ] = field.find( "align" )
                    d[ "tip" ] = field.find( "tip" )

                    for key in d:
                        if d[ key ] != None:
                            d[ key ] = d[ key ].text

                    d[ "value" ] = ""

                    t.fields.append( d )

                self.tabs.append( t )
