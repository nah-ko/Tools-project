#!/bin/bash
#
# Script de dump global a utiliser en tant que user postgres. Il permet
# de dumper toutes les bases et egalement celles ayant des large object.
# On indique en parametres le nom du fichier ainsi que le couple
# base/table lorsqu'il s'agit de dumper les large object.

# $Id$

PROG=`basename $0`
NO_ARGS=0
E_OPTERROR=65

usage() {
cat << EOF

$PROG, dump all databases including those who contains large object

Usage : $PROG -p PREFIX_FILENAME [-d DBNAME -t TABLENAME]
    -p PREFIX_FILENAME	    Give a prefix to output filename.
    -d DBNAME		    Name of database containing large object. Need -t.
    -t TABLENAME	    Give the table name where large object are.
    -v			    Verbose

EOF
    exit $E_OPTERROR
}

if [ $# -eq "$NO_ARGS" ]
then    
    usage
fi

while getopts ":p:d:t:" OPTIONS
do
    case $OPTIONS in
	v)
	    VERBOSE=true
	    ;;
	*)
	    echo "No matching option, retry."
	    usage
	    ;;
	:)
	    echo "Missing parameter for $OPTARG"
	    exit 1
	    ;;
    esac
done

