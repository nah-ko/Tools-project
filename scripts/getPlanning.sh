#! /usr/bin/env bash
# Recuperation du planning hebdo pour envoi par mail.

# $Id$

PATH=/usr/bin:/bin:/usr/local/bin

# Creation d'un fichier temporaire.
PLANNING=/tmp/$$

# Url du planning a recuperer.
URL=http://url-of-planning.domain.tld

# Expediteur et destinataire du mail.
EXPE=user@domain.tld
DEST=user@otherdomain.tld
OBJET="Planning"

# Recuperation, envoi du planning suivi de l'effacement du fichier
# temporaire.
/usr/bin/links -dump '$URL' | tail -20 | sed -r 's/^.{23}//g' > $PLANNING
/bin/cat $PLANNING | /usr/bin/mail -s $OBJET -a "From: $EXPE" $DEST
rm $PLANNING
