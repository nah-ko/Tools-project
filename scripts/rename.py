#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-
#
# rename files, unaccent and lower case old name
#
# $Id: rename.py,v 1.4 2004/05/03 08:36:45 dim Exp $

def unacc_table():
    """ Provide a translate table for removing of accents in input """
    table = ""
    for i in range(0, 256):
        old = chr(i)
        if old.isspace() or old in '(){}[]<>@$*%!?,;:+=-#~&`|\\\'"':
            new = '_'
	elif old in 'áàäâã':
	    new = 'a'
        elif old in 'ÁÀÄÂÃ':
            new = 'A'
	elif old in 'éèêë':
	    new = 'e'
	elif old in 'ÉÈÊË':
	    new = 'E'
	elif old in 'ìíîï':
	    new = 'i'
	elif old in 'ÌÍÎÏ':
	    new = 'I'
	elif old in 'òóôõö':
	    new = 'o'
	elif old in 'ÒÓÔÕÖ':
	    new = 'O'
	elif old in 'ùúûü':
	    new = 'u'
	elif old in 'ÙÚÛÜ':
	    new = 'U'
	elif old in 'ç':
	    new = 'c'
	elif old in 'Ç':
	    new = 'C'
	else:
	    new = chr(i)
	
	table = table + new

    return table

if __name__ == "__main__":
    import sys, os
    from optparse import OptionParser

    # Create the tranlation table.
    table = unacc_table()

    # Organize options.
    myoptions = OptionParser("%prog [options] source")
    myoptions.add_option("-s", "--simulate", dest="simulate", help="Do not rename files, just give preview of the operation.", action="store_true", default=False)
    myoptions.add_option("-i", "--interactive", dest="interactive", help="Ask before renaming a file.", action="store_true", default=False)
    myoptions.add_option("-q", "--quiet", dest="verbose", help="Be quiet. Default is to print operation.", action="store_false", default=True)
    (options, args) = myoptions.parse_args()

    # Program take only one argument, source filename.
    if len(args) != 1:
	myoptions.print_help()
	sys.exit(2)

    # Get source filename.
    Source = args[0]
    Destination = Source.translate(table).lower()

    #if options.verbose:
	#print "Simulate: %s, Interactive: %s, Verbose: %s" % (options.simulate, options.interactive, options.verbose)
	#print "Args: %s" % args
	#print "Source: %s" % Source
    
    # Interactivly rename filename
    if options.interactive:
	Response = 'rien'
	while Response not in 'YyNn':
	    Response = raw_input('Do you really want to rename %s as %s ?  [Y/n]: ' % ( Source, Destination ))
	if Response in 'Yy':
	    if options.verbose:
		print "Renaming %s as %s" % ( Source, Destination )
		if options.simulate:
		    print "Simulation done."
		    sys.exit(0)
		else:
		    os.rename( Source, Destination )
		    print "Done."
	else:
	    print "Renaming aborted..."
    # Simulate the renaming process
    elif options.simulate:
	print "Renaming %s as %s\nSimulation done." % ( Source, Destination )
	sys.exit(0)
    else:
	if options.verbose:
	    print "Renaming %s as %s" % ( Source, Destination )
	os.rename( Source, Destination )
	print "Done."
