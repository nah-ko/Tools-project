#!/usr/bin/env python
#
# Script permettant de donner le temps ecoule entre deux appels
#

# $Id$

import os, time, email, sys

progname = sys.argv[0]
timefile = '/tmp/elapsedtime'
logfile  = '/home/toffe/public_html/log_adsl'
sender   = 'toffe@nah-ko.org'
receiver = sender

# recuperation du suffix permettant l'ordonnancement
# le nom sera donc: elapsedtime-{up|down}.py
# [0] sur le premier split pour avoir le nom sans l'extension
# [1] sur le second pour obtenir le suffixe
suffix = progname.split('.')[0].split('-')[1]

# on considere que c'est le premier lancement.
# (pas de timefile, suffix a up)
if not os.path.exists(timefile) and suffix == 'up':
    start = time.time()
    fd = open(timefile, "w+")
    fd.write(str(start))
    fd.close()
# on le lit pour faire le calcul.
# (timefile cree precedemment, suffix a down)
elif os.path.exists(timefile) and suffix == 'down':
    # recuperation du timestamp
    fd = open(timefile, "r")
    start = float(fd.readlines()[0])
    fd.close()
    # calcul du temps ecoule
    end   = time.time()
    elapsed_time = time.gmtime( end - start )
    elapsed_hour = elapsed_time[3]
    elapsed_min  = elapsed_time[4]
    elapsed_sec  = elapsed_time[5]
    if elapsed_time[2] > 1:
	elapsed_hour += 24 * ( elapsed_time[2] - 1 )
    os.remove(timefile)
    # creation du message
    message = "%d hour(s) %d minute(s) %d second(s)" % (elapsed_hour, elapsed_min, elapsed_sec)
    fd = open(logfile, "a+")
    fd.write(message+"\n")
    fd.close()
    # envoi du message par mail
    import smtplib
    from email.MIMEText import MIMEText
    msg = MIMEText(message)
    msg['Subject'] = 'xDSL reconnection'
    msg['From']    = sender
    msg['To']      = receiver
    s = smtplib.SMTP()
    s.connect()
    s.sendmail(sender, receiver, msg.as_string())
    s.close()
