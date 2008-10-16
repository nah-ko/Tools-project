#!/bin/bash
#
# Script de dump global a utiliser en tant que user postgres. Il permet
# de dumper toutes les bases et egalement celles ayant des large object.
# On indique en parametres le nom du fichier ainsi que le couple
# base/table lorsqu'il s'agit de dumper les large object.

# $Id$

PATH=/bin:/usr/bin:/usr/lib/postgresql/bin

TODAY=`date -I`
PROG=`basename $0`
PROG_PATH=`dirname $0`
#DUMP_PATH=`dirname $0` # a decommenter si l'on desire mettre les dump ailleurs.
/usr/bin/test -n "$DUMP_PATH" || DUMP_PATH=$PROG_PATH
A=`which pg_dumpall`
DA_PATH=`dirname $A`
A=`which pg_dump`
DLO_PATH=`dirname $A`
/usr/bin/test -n "$DA_PATH" || DA_PATH="/usr/lib/postgresql/bin"

BZIP2=`which bzip2`
BZOPT="-z9f"

NO_ARGS=0
E_OPTERROR=65

PREFIX_FILENAME=NoPrefix_
# Par defaut cette variable est vide => connection via une socket pour
# eviter le pb avec identd (MYHOSTNAME="--host=localhost")
MYHOSTNAME=""
# Idem, variable vide par defaut, si necessaire il faut indiquer quel
# cluster est a sauvegarder
MYCLUSTER=""
DBNAME=template1
TABLENAME=pg_database

VERBOSE=false

usage() {
cat << EOF

$PROG, dump all databases including those who contains large object

Usage : $PROG -p PREFIX_FILENAME [-l DBNAME/TABLENAME -v]
    -p PREFIX_FILENAME	    Give a prefix to output filename.
    -h HOSTNAME             Same as pg_dump and pg_dumpall
    -l DBNAME/TABLENAME	    Give the name of database and table where to
			    dump large object. You may have two or more
			    couple here. Then you'll need to put it into
			    doublequote (eg "db1/tbl1 db2/tbl2")
    -v			    Verbose, dumping will use the verbose mode

EOF
    exit $E_OPTERROR
}

warning() {
cat << EOF

!! WARNING !!
You have dumped databases in which where stored large objects, in order
to restore them correctly you will have to do some special operations.

1- Be sure that those tables are empty, if not do a TRUNCATE TABLE
yourtable.

2- Use correct options for restoration, large object database will need
only the format option: -Fc (see stdout for informations about used
commands).

These information are important since you've done a restore of the whole
SQL server with the pg_dumpall dump before. Otherwise dropping tables
and sequences before restoring them must be efficient.

EOF
}

DumpAll() {
    # Default options: -c Include SQL commands to clean (drop) the
    # databases before recreating them. -i Ignore version mismatch
    # between  pg_dumpall  and  the  database server. Read pg_dumpall
    # manpage for more informations.
    DA_opts="$MYHOSTNAME $MYCLUSTER -c -i"
    $VERBOSE && DA_opts=`echo $DA_opts -v`
    $VERBOSE && echo "--- Global dump ---"
    $VERBOSE && echo "pg_dumpall $DA_opts > $DUMP_PATH/${PREFIX}_DumpAll_$TODAY.out"
    $DA_PATH/pg_dumpall $DA_opts > $DUMP_PATH/${PREFIX}_DumpAll_$TODAY.out
}

DumpLO() {
    # Default options: -Fc Selects the format of the output. Output a
    # custom archive suitable for input into pg_restore. -b Include large
    # objects in dump. -o Dump object identifiers (OIDs) for every
    # table. -c Output  commands  to clean (drop) database objects prior
    # to (the commands for) creating them. -C Begin the output with a
    # command to create  the  database  itself and  reconnect  to  the
    # created database. -s Dump only the schema (data definitions), no
    # data. -a Dump only the data, not the schema (data definitions).
    # Read pg_dump manpage for more informations.
    DLO_opts="$MYHOSTNAME $MYCLUSTER -i -Fc"
    $VERBOSE && DLO_opts=`echo $DLO_opts -v`
    for ARGS in $LO_NAMES
    do
	eval `echo $ARGS | sed -r 's/^(.*)\/(.*)$/DBNAME=\1 TBLNAME=\2/g'`
	$VERBOSE && echo "--- Schema dump of ${DBNAME} ---"
	opts=`echo $DLO_opts -cCs`
	$VERBOSE && echo "pg_dump $opts ${DBNAME} > $DUMP_PATH/${PREFIX}_${DBNAME}-${TBLNAME}_DumpLOschema_$TODAY.out"
	$DLO_PATH/pg_dump $opts ${DBNAME} > $DUMP_PATH/${PREFIX}_${DBNAME}-${TBLNAME}_DumpLOschema_$TODAY.out
	$VERBOSE && echo "--- Data dump of ${DBNAME} ---"
	opts=`echo $DLO_opts -abo`
	$VERBOSE && echo "pg_dump $opts ${DBNAME} > $DUMP_PATH/${PREFIX}_${DBNAME}-${TBLNAME}_DumpLOdata_$TODAY.out"
	$DLO_PATH/pg_dump $opts ${DBNAME} > $DUMP_PATH/${PREFIX}_${DBNAME}-${TBLNAME}_DumpLOdata_$TODAY.out
    done
}

# Main code
if [ $# -eq "$NO_ARGS" ]
then    
    usage
fi

while getopts ":c:dvh:p:l:" OPTIONS
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
	h)
	    MYHOSTNAME="--host=$OPTARG"
	    ;;
	c)
	    MYCLUSTER="--cluster $OPTARG"
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
    warning
fi

$VERBOSE && BZOPT="-z9vf"

$BZIP2 $BZOPT $DUMP_PATH/${PREFIX}*.out
find $DUMP_PATH/ -type f -follow -mtime +7 -name "*.out.bz2" -exec rm -v {} \;
