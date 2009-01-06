#!/usr/bin/env python

import Image, os, re, sys, getopt
import pg
from optparse import OptionParser

# Default values
ProgPath  = os.path.dirname(os.path.realpath(sys.argv[0]))
ConfFile  = ProgPath + "/image2db.conf"
HOST      = "localhost"
PORT      = 5432
img_db    = "Images"
img_dbus  = "image"
img_dbpw  = "passwd"
img_table = "imgtable"
img_tblsq = "imgtable_id_seq"
file      = None
desc      = None

def ReadConf( configuration_file = ConfFile ):
   """ Read configuration file """
   
   import ConfigParser
   global HOST, PORT
   global img_db, img_dbus, img_dbpw, img_table, img_tblsq

   config = ConfigParser.ConfigParser()
   config.read(configuration_file)

   # Reading options
   HOST      = config.get('GLOBAL', 'host')
   PORT      = int(config.get('GLOBAL', 'port'))
   img_db    = config.get('GLOBAL', 'img_db')
   img_dbus  = config.get('GLOBAL', 'img_dbus')
   img_dbpw  = config.get('GLOBAL', 'img_dbpw')
   img_table = config.get('GLOBAL', 'img_table')
   img_tblsq = config.get('GLOBAL', 'img_tblsq')

def InsertFile(myfile, mydesc):
   """ Add image to database """

   if myfile == None:
      print "No <file> !"
      sys.exit(2)

   print "We're going to add %s to %s" % (myfile, img_table)

   PATH    = os.path.dirname(myfile)
   if PATH == "":
   	PATH = "./"
   INFILE  = os.path.basename(myfile)
   OUTFILE = PATH + "/tn_" + INFILE
   X       = 120
   Y       = 90
   size    = os.stat(myfile).st_size
   type_   = Image.open(myfile).format

   # Getting image data
   f        = open(myfile,"r")
   img_data = f.read()
   f.close()
   # Create thumbnail and get data
   i        = Image.open(myfile)
   i.thumbnail((X,Y))
   i.save(OUTFILE,type_)
   f        = open(OUTFILE,"r")
   tn_data  = f.read()
   f.close()

   # Put images into DB
   try:
      db = pg.connect(dbname=img_db, host=HOST, port=PORT, user=img_dbus, passwd=img_dbpw)
   except pg.InternalError, connectError:
      print "CONNECT PROBLEM:\r\n %s\n" % connectError
      print "Please correct %s and retry\n" % ConfFile
      sys.exit(2)

   # begin operation
   db.query("begin")
   img_lo = db.locreate(pg.INV_WRITE)
   tn_lo  = db.locreate(pg.INV_WRITE)
   # Insertion des donnees
   type   = "image/"+type_
   req    = db.query("insert into %s (image, thumbnail, description, filename, filesize, filetype) values ('%s', '%s', '%s', '%s', '%s', '%s')" % (img_table, img_lo.oid, tn_lo.oid, mydesc, INFILE, size, type))
   # Ecriture dans les LO
   img_lo.open(pg.INV_WRITE)
   img_lo.write(img_data)
   img_lo.close()
   tn_lo.open(pg.INV_WRITE)
   tn_lo.write(tn_data)
   tn_lo.close()
   # Fin de transaction
   db.query("commit")
   id = db.query("select currval('%s')" % img_tblsq).getresult()[0][0]
   print "%s added with id : %s" % (INFILE, id)
   db.close()

def main():
   """ Main code """

   global file, desc, ConfFile
   global CONFIG_FILE, SCREENSHOT_FILE, DESCRIPTION

   Usage = " Usage: %prog -f image -d description [-h] [-c config] "
   Parser = OptionParser(usage = Usage)
   Parser.add_option("-f", "--screenshotfile",
                     action = "store",
		     type   = "string",
		     dest   = "ShotFile",
		     metavar = "SHOTFILE",
		     default = SCREENSHOT_FILE,
		     help    = "Path to the screenshot file")
   Parser.add_option("-d", "--description",
                     action = "store",
		     type   = "string",
		     dest   = "Description",
		     metavar = "DESC",
		     default = DESCRIPTION,
		     help    = "Description of the screenshot")
   Parser.add_option("-c", "--configfile",
                     action = "store",
		     type   = "string",
		     dest   = "Conf_File",
		     metavar = "FILE",
		     default = CONFIG_FILE,
		     help    = "Path to the configuration file")
   (options, args) = Parser.parse_args()

   # Use configuration file given or default one
   if os.path.exists(options.Conf_File):
   	ConfFile = options.Conf_File
   else:
   	Parser.error( "Sorry, configuration file \"%s\" "\
		      "missing or unreadable"\
		      % options.Conf_File)

   # Use given screenshot file
   if os.path.exists(options.ShotFile):
   	file = options.ShotFile
   elif len(options.ShotFile) == 0:
   	Parser.error( "No image !" )
   else:
   	Parser.error( "Sorry, image file \"%s\" "\
		      "missing or unreadable"\
		      % options.ShotFile )
 
   # Get description for screenshot
   if len(options.Description) > 0:
   	desc = options.Description
   else:
	Parser.error( "No description or empty description" )
   
   ReadConf(ConfFile)
   InsertFile(file, desc)

if __name__ == "__main__":
   global CONFIG_FILE, DESCRIPTION, SCREENSHOT_FILE

   ProgPath     = os.path.dirname(os.path.realpath(sys.argv[0]))
   CONFIG_FILE  = ProgPath + "/image2db.conf"
   DESCRIPTION  = ""
   SCREENSHOT_FILE = ""

   main()
