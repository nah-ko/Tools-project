#!/bin/bash
#
# script de generation de planche contact (autrement appelle index) a
# l'aide de la commande montage de ImageMagick
#

# $Id$

FICHIERS=$1
PLANCHECONTACT=$2

montage -verbose \
        -label "%f" \
        -background black \
	-fill yellow \
	-bordercolor white \
	-border +2 \
	-geometry 320x240 \
	$FICHIERS $PLANCHECONTACT
