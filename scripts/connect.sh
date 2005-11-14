#!/bin/bash
#
# $Id$
#
# Se connecter depuis la clef et une machine linux sur des machines avec
# lesquelles j'ai echange une clef.

MYSSH=`which ssh`
PROGNAME=`dirname $0`
MYSSHKEY=$PROGNAME/clef_ssh/travelkey-RSA2048

chmod 600 $MYSSHKEY

$MYSSH -t -i $MYSSHKEY $*
