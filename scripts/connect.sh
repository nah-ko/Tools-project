#!/bin/bash
#
# $Id: connect.sh,v 1.1 2005/11/14 15:49:57 toffe Exp $
#
# Se connecter depuis la clef et une machine linux sur des machines avec
# lesquelles j'ai echange une clef.

MYSSH=`which ssh`
PROGNAME=`dirname $0`
MYSSHKEY=$PROGNAME/clef_ssh/travelkey-RSA2048

chmod 600 $MYSSHKEY

$MYSSH -t -i $MYSSHKEY $*
