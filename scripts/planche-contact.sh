#!/bin/bash
#
# script de generation de planche contact (autrement appelle index) a
# l'aide de la commande montage de ImageMagick
#

# $Id$

FICHIERS=$1
PLANCHECONTACT=$2

montage -label "%f" \
        -background black \
	-fill yellow \
	-bordercolor white \
	-borderwidth +2 \
	$FICHIERS $PLANCHECONTACT
