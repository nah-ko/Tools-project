#!/usr/bin/env python

import httplib, urllib, os
import sys, string, locale
import ConfigParser
from HTMLParser import HTMLParser
from optparse import OptionParser

class MonParseurHTML( HTMLParser ):

	def __init__(self):
		HTMLParser.__init__(self)
		self.in_dico = False
		self.current_def = None
		self.current_tag = None
		self.tableau = []
		self.ligne = ()
		self.keepdata = False
		self.indice = 0

	def handle_starttag(self, tag, attrs):
		self.current_tag = tag
		if tag == 'td':
			for (attr, val) in attrs:
				if attr == 'class' and val in ( 'dta_cell', 'dta_header' ):
				# les cellules a garder contiennent
				# dta_cell ou dta_header dans le nom de
				# la classe
					self.in_dico = True
		
		if self.in_dico and self.current_tag == 'p':
		# la donnee elle meme est dans un tag p
			self.keepdata = True

	def handle_endtag(self, tag):
		self.current_tag = None
		if tag == 'td':
			self.in_dico = False

	def handle_data(self, data):
		if self.in_dico and self.keepdata and data <> '\n' and self.indice < NBCOLS:
			self.ligne += (data,)
			self.indice += 1
		elif self.indice == NBCOLS:
			self.tableau.append(self.ligne)
			self.indice = 0
			self.ligne = ()

	def close(self):
		HTMLParser.close(self)
		if self.current_def is not None:
			print_def(self.current_def, self.accu)

		return self.tableau

def ReadConf (configfile = "GetNerimAccounting.conf"):
	global HOST, URL, AUTH

	SECTION = 'DEFAULT'

	# ouverture du fichier pour lecture de la conf
	config = ConfigParser.ConfigParser()
	config.read(configfile)

	# recuperation des options
	if config.has_option(SECTION, 'AUTH'):
		AUTH = config.get(SECTION, 'AUTH')
		# transformation de la chaine de caracteres en un
		# dictionnaire tel qu'on en a besoin pour l'encodage de
		# l'url
		AUTH = dict([(x[0].strip(), x[1].strip()) for x in [y.strip().split(":") for y in AUTH.strip('{}').split(",")]])
	if config.has_option(SECTION, 'HOST'):
		HOST = config.get(SECTION, 'HOST')
	if config.has_option(SECTION, 'URL'):
		URL = config.get(SECTION, 'URL')

def GetAccounting():
	global AUTH, HOST, URL

	parametres = urllib.urlencode(AUTH)
	entetes = {"Content-type": "application/x-www-form-urlencoded",
	           "Accept": "text/plain"}

	connection = httplib.HTTPSConnection(HOST)
	connection.request( "POST", URL, parametres, entetes )
	reponse = connection.getresponse()
	#print reponse.status, reponse.reason
	pagehtml = reponse.read()
	connection.close()

	return pagehtml

if __name__ == "__main__":
	# variables indispensables
	AUTH = {"login": "marcel", "password": "etsonorchestre", "realm": "cherchelycos"}
	HOST = "admin.monfai.net"
	URL  = "/chemin/de/la/page/accounting/radius"

	ProgPath     = os.path.dirname(os.path.realpath(sys.argv[0]))
	CONFIG_FILE  = ProgPath + "/NerimAccounting.conf"

	# nombre de colonnes du tableau de la page
	NBCOLS = 7

	# Options du programme
	Usage = "Usage: %prog [options]"
	Parser = OptionParser(usage = Usage)
	Parser.add_option("-c", "--configfile",
	                  action  = "store",
			  type    = "string",
			  dest    = "ConfFile",
			  metavar = "FILE",
			  default = CONFIG_FILE,
			  help    = "Chemin d'acces au fichier de configuration")
	(options, args) = Parser.parse_args()

        if os.path.exists(options.ConfFile):
		config_file = options.ConfFile
	else:
		confErrMsg  = "Desole, le fichier de configuration %s "\
			      "n'existe pas ou est illisible, nous "\
			      "utiliserons celui par defaut a la place " \
			      % options.ConfFile
		config_file = CONFIG_FILE
	
	# lecture de la conf
	ReadConf(config_file)
	p = MonParseurHTML()
	p.feed(GetAccounting())
	T = p.close()
	iL = 0
	while iL < len(T):
		print "%s\t%s\t%s\t%s" % (T[iL][0], T[iL][1], T[iL][2], T[iL][3])
		iL += 1

