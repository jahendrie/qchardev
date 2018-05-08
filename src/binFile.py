import lzma, pickle
import xml.etree.ElementTree as ET

dAlignTypes = {
        "horizontal" : 0,
        "vertical" : 1 }

dFieldTypes = {
        "short" : 0,
        "long" : 1,
        "radio" : 2,
        "multiple" : 3
        }


class BinFile():
    def __init__( self ):

        self.path = ""
        self.template = None
        self.characters = None


def save_file( path, zTemplate, characters ):

    ##  Create the file, set the path
    bf = BinFile()
    bf.path = path

    fout = open( bf.path, "wb" )

    ##  Template
    #bf.template = read_template( templatePath )
    bf.template = bytes.decode( lzma.decompress( zTemplate ), "utf-8" )

    ##  Setting the characters
    bf.characters = characters

    b = pickle.dumps( bf )
    z = lzma.compress( b )

    fout.write( z )
    fout.flush()
    fout.close()



def get_template_from_save( path ):


    fin = open( path, "rb" )
    z = fin.read()
    fin.close()

    b = lzma.decompress( z )
    bf = pickle.loads( b )

    return( bf.template )




def read_template( tPath ):
    fin = open( tPath, "r" )
    txt = fin.read()
    fin.close()

    return( txt )


def compress_template( tPath ):

    fin = open( tPath, "r" )
    txt = fin.read()
    fin.close()

    z = lzma.compress( bytes( txt, "utf-8" ) )

    return( z )



def load_file( path ):

    ##  Read the compressed file
    fin = open( path, "rb" )
    z = fin.read()
    fin.close()

    ##  Decompress it
    b = lzma.decompress( z )

    ##  Unpickle it
    bf = pickle.loads( b )

    ##  Get the textual template
    template = ET.fromstring( bf.template )
    zTemplate = lzma.compress( bytes( bf.template, "utf-8" ))

    ##  Return stuff
    return( template, zTemplate, bf.characters )
