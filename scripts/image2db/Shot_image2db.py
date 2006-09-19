#!/usr/bin/env python

import Image, os, re, sys, getopt
import pg

# Default values
ProgPath  = os.path.dirname(os.path.realpath(sys.argv[0]))
ConfFile  = ProgPath + "/image2db.conf"
HOST      = "localhost"
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
   global HOST
   global img_db, img_dbus, img_dbpw, img_table, img_tblsq

   config = ConfigParser.ConfigParser()
   config.read(configuration_file)

   # Reading options
   HOST      = config.get('GLOBAL', 'host')
   img_db    = config.get('GLOBAL', 'img_db')
   img_dbus  = config.get('GLOBAL', 'img_dbus')
   img_dbpw  = config.get('GLOBAL', 'img_dbpw')
   img_table = config.get('GLOBAL', 'img_table')
   img_tblsq = config.get('GLOBAL', 'img_tblsq')

def InsertFile(myfile, mydesc):
   """ Add image to database """

   if myfile == None:
      print "No <file> !"
      usage()
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
      db = pg.connect(dbname=img_db, host=HOST, user=img_dbus, passwd=img_dbpw)
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

def usage():
   """ Give usage if needec """
   command = os.path.basename(sys.argv[0])
   print "%s -f <image_file> -d <description>" % command

def main():
   """ Main code """

   global file, desc, ConfFile

   try:
      opts, args = getopt.getopt(sys.argv[1:], "f:d:c:")
   except getopt.GetoptError:
      # print help information and exit:
      usage()
      sys.exit(2)

   for o, a in opts:
      if o == "-c":
         if os.path.exists(a):
            ConfFile = a
	 else:
	    print "Configuration file %s does not exists" % a
	    usage()
	    sys.exit(2)
      elif o == "-f":
         if os.path.exists(a):
            file = a
	 else:
	    print "%s: File does not exists" % a
	    usage()
	    sys.exit(2)
      elif o == "-d":
         desc = a
   
   ReadConf(ConfFile)
   InsertFile(file, desc)

if __name__ == "__main__":
	main()
