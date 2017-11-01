#! /bin/sh
# Script de backup d'une arbo CVSROOT

# $Id: BackupCvs.sh,v 1.1 2004/06/25 14:54:33 toffe Exp $

# Chemin d'acces aux programmes et fichiers
PATH=$HOME/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/X11R6/bin
PROGPATH=`dirname $0`

# Fichier contenant la liste des fichiers et repertoires exclus, selon
# le contenu on peut ne backuper qu'une partie des fichiers. Exemple:
# EXCLUDEFILE=$PROGPATH"/rsync_exclude_global.conf" permet un backup
# global.
EXCLUDEFILE=$PROGPATH"/rsync_exclude.conf"

# La source peut etre une machine distante avec laquelle il y a eu un
# echange de clefs ssh: SOURCE='user@domain.tld:/dir/of/web/datas/'
DESTINATION=$HOME/dev/perso/MyCVSROOT/
SOURCE=/location/of/CVSROOT/

echo "Lancement `date`"
echo "Program path: $PROGPATH, exclude file: $EXCLUDEFILE"
/usr/bin/rsync -avz -e ssh --bwlimit=2 --delete-after --exclude-from=$EXCLUDEFILE $SOURCE $DESTINATION
