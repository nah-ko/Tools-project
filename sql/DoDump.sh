#!/bin/bash
#
# Script de dump global a utiliser en tant que user postgres. Il permet
# de dumper toutes les bases et egalement celles ayant des large object.
# On indique en parametres le nom du fichier ainsi que le couple
# base/table lorsqu'il s'agit de dumper les large object.

# $Id$

#set -x

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

DumpAll() {
    # Default options: -c Include SQL commands to clean (drop) the
    # databases before recreating them. -i Ignore version mismatch
    # between  pg_dumpall  and  the  database server. Read manpage for
    # pg_dumpall for more informations.
    DA_opts="-c -i"
    if [ $VERBOSE ]
    then
	DA_opts=`echo $DA_opts -v`
    fi
    echo "pg_dumpall $DA_opts > ${PREFIX}_DumpAll.`date -I`.out"
}

DumpLO() {
    DLO_opts="-Ft -b -o -c -C"
    if [ $VERBOSE ]
    then
	DLO_opts=`echo $DLO_opts -v`
    fi
    echo "pg_dump $DLO_opts > ${PREFIX}_${DBNAME}-${TBLNAME}_DumpLO.`date -I`.out"
}

# Main code
if [ $# -eq "$NO_ARGS" ]
then    
    usage
fi

while getopts ":vp:d:t:" OPTIONS
do
    case $OPTIONS in
	v)
	    VERBOSE=true
	    ;;
	p)
	    PREFIX=$OPTARG
	    ;;
	d)
	    DBNAME=$OPTARG
	    ;;
	t)
	    TBLNAME=$OPTARG
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

DumpAll
if [ "$DBNAME" != "" -a "$TBLNAME" != "" ]
then
    DumpLO
else
    echo "No large object to dump."
fi
