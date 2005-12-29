#!/bin/bash
#
# script de generation de planche contact (autrement appelle index) a
# l'aide de la commande montage de ImageMagick
#

# $Id$

FICHIERS=$1
PLANCHECONTACT=$2

montage -verbose \
        -label "APN: %[EXIF:Model] - Date: %[EXIF:DateTime]\nIso: %[EXIF:ISOSpeedRatings] - Ouverture: %[EXIF:ApertureValue]\nFocale: %[EXIF:FocalLength] - Temps de pose: %[EXIF:ExposureTime]" \
        -background black \
	-fill yellow \
	-bordercolor white \
	-border +2 \
	-geometry 800x600+5+5 \
	$FICHIERS $PLANCHECONTACT
