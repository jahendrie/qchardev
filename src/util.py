import sys, os

##  Globals
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800

VERSION = "0.90"



def system_install_path():
    return( "/usr/share/qytdl" )


def get_data_dir():

    ##  If they're on windows
    if sys.platform == "win32" or sys.platform == "win64":
        dataDir = "%s\\data" % (
                os.path.abspath( "%s\\.." % os.path.dirname( sys.argv[0] )) )

    ##  Otherwise, we assume linux / unix
    else:
        dataDir = "%s/data" % (
                os.path.abspath( "%s/.." % os.path.dirname( sys.argv[0] )) )

    return( dataDir )


def recents_path():
    if sys.platform == "win32" or sys.platform == "win64":
        return( "%s\\recents" % get_data_dir() )
    else:
        return( "%s/recents" % get_data_dir() )




def icon_path( filename = "", systemInstall = False ):

    if systemInstall:
        return( "/usr/share/qytdl/data/icons" )

    ##  Check for Windows
    if sys.platform == "win32" or sys.platform == "win64":
        return( "%s\\icons\\%s" % ( get_data_dir(), filename ))

    ##  Otherwise, we assume linux / unix
    else:
        return( "%s/icons/%s" % ( get_data_dir(), filename ))


def image_path( filename = "" ):

    if sys.platform == "win32" or sys.platform == "win64":
        return( "%s\\images\\%s" % ( get_data_dir(), filename ))

    else:
        return( "%s/images/%s" % ( get_data_dir(), filename ))


def downloads_path():


    home = os.getenv( "HOME" )
    winPaths = ( "%s\\Downloads" % home, "%s\\downloads" % home )
    linPaths = ( "%s/Downloads" % home, "%s/downloads" % home )


    if sys.platform == "win32" or sys.platform == "win64":
        return( sys_downloads_path( winPaths ))

    else:
        return( sys_downloads_path( linPaths ))


def sys_downloads_path( paths ):
        for p in paths:
            if os.path.exists( p ):
                return( p )
        return( home )



def template_path():

    if sys.platform == "win32" or sys.platform == "win64":
        return( "%s\\template.xml" % get_data_dir() )
    else:
        return( "%s/template.xml" % get_data_dir() )


def export_path():
    if sys.platform == "win32" or sys.platform == "win64":
        return( "%s\\export" % get_data_dir() )
    else:
        return( "%s/export" % get_data_dir() )


def get_free_space( path ):

    try:
        s = os.statvfs( path )
    except ( PermissionError, FileNotFoundError ):
        return( "UNKNOWN" )

    suffices = ( 'bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB' )
    suffix = 0
    freeSpace = s.f_frsize * s.f_bavail

    ##  Get it down to a sane number
    while( freeSpace > 1024 ):
        freeSpace /= 1024
        suffix += 1

    ##  Just to be safe, I guess
    if suffix >= len( suffices ):
        freeSpace = s.f_frsize * s.f_bavail
        suffix = 0

    if suffix > 0:
        freeSpaceStr = "%.02f %s" % ( freeSpace, suffices[ suffix ] )
    else:
        freeSpaceStr = "%d bytes" % freeSpace

    return( freeSpaceStr )


