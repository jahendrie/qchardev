from util import *

class Recents():

    def __init__( self ):

        self.recentsPath = "%s/recents.dat" % get_data_dir()


    def load_recents( self ):

        recents = []

        try:
            fp = open( self.recentsPath, "rb" )

            ##  First byte:  number of recents, max 10
            numRecents = int.from_bytes( fp.read( 4 ), "little", signed=False )

            ##  Each path is two parts:  Its length (1 unsigned byte), and
            ##  its string
            for r in range( numRecents ):
                size = int.from_bytes( fp.read( 4 ), "little", signed=False )
                path = fp.read( size ).decode( "ascii" )

                recents.append( path )

        except IOError:
            try:
                fp = open( self.recentsPath, "wb" )
                fp.close()
            except IOError:
                print( "ERROR:  Could not open recents file for reading" )


        return( recents )
    

    def append_recent( self, path ):

        recents = self.load_recents()
        if len( recents ) >= 10:
            del recents[ 0 ]

        if path in recents:
            del recents[ recents.index( path ) ]

        recents.append( path )

        try:
            fp = open( self.recentsPath, "wb" )

            ##  Write the number of recents
            fp.write( ( len(recents) ).to_bytes( 4, "little", signed=False ))

            ##  For each one, write its length and the string itself
            for r in recents:
                fp.write( ( len(r) ).to_bytes( 4, "little", signed=False ))
                fp.write( r.encode( "ascii" ))

        except IOError:
            print( "ERROR:  Could not open recents file for writing" )
