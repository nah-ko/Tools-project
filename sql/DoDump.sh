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

Usage : $PROG -p PREFIX_FILENAME [-l DBNAME/TABLENAME -v]
    -p PREFIX_FILENAME	    Give a prefix to output filename.
    -l DBNAME/TABLENAME	    Give the name of database and table where to
			    dump large object. You may have two or more
			    couple here. Then you'll need to put it into
			    doublequote (eg "db1/tbl1 db2/tbl2")
    -v			    Verbose, dumping will use the verbose mode

EOF
    exit $E_OPTERROR
}

DumpAll() {
    # Default options: -c Include SQL commands to clean (drop) the
    # databases before recreating them. -i Ignore version mismatch
    # between  pg_dumpall  and  the  database server. Read pg_dumpall
    # manpage for more informations.
    DA_opts="-c -i"
    if [ $VERBOSE ]
    then
	DA_opts=`echo $DA_opts -v`
    fi
    echo "pg_dumpall $DA_opts > ${PREFIX}_DumpAll.`date -I`.out"
}

DumpLO() {
    # Default options: -Ft Selects the format of the output. Here it's a
    # tar archive suitable for input into  pg_restore. -b Include large
    # objects in dump. -o Dump object identifiers (OIDs) for every
    # table. -c Output  commands  to clean (drop) database objects prior
    # to (the commands for) creating them. -C Begin the output with a
    # command to create  the  database  itself and  reconnect  to  the
    # created database. Read pg_dump manpage for more informations.
    DLO_opts="-Ft -b -o -c -C"
    if [ $VERBOSE ]
    then
	DLO_opts=`echo $DLO_opts -v`
    fi
    for ARGS in $LO_NAMES
    do
	eval `echo $ARGS | sed -r 's/^(.*)\/(.*)$/DBNAME=\1 TBLNAME=\2/g'`
	echo "pg_dump $DLO_opts > ${PREFIX}_${DBNAME}-${TBLNAME}_DumpLO.`date -I`.out"
    done
}

# Main code
if [ $# -eq "$NO_ARGS" ]
then    
    usage
fi

while getopts ":vp:l:" OPTIONS
do
    case $OPTIONS in
	d)
	    set -x
	    ;;
	v)
	    VERBOSE=true
	    ;;
	p)
	    PREFIX=$OPTARG
	    ;;
	l)
	    LO_NAMES=$OPTARG
	    ;;
	*)
	    echo "No matching option for -$OPTARG, retry."
	    usage
	    ;;
	:)
	    echo "Missing parameter for $OPTARG"
	    exit 1
	    ;;
    esac
done

DumpAll
if [ "$LO_NAMES" != "" ]
then
    DumpLO
else
    echo "No large object to dump."
fi
