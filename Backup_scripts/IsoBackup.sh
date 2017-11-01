#! /bin/sh
# Generation d'iso pour sauvegarde sur CD/DVD

# $Id: IsoBackup.sh,v 1.1 2005/06/10 13:27:23 toffe Exp $

REP=$1

/usr/bin/mkisofs -R -r -J -joliet-long --hide-rr-moved -V SVG_`date -I` -o /opt/sauvegardes/SVG_`date -I`.iso $REP
