#!/usr/bin/env python
#
# Script permettant de donner le temps ecoule entre deux appels
#

# $Id$

import os, time

timefile = '/tmp/elapsedtime'

if not os.path.exists(timefile):
    start = time.time()
    fd = open(timefile, "w+")
    fd.write(str(start))
    fd.close()
else:
    fd = open(timefile, "r")
    start = float(fd.readlines()[0])
    fd.close()
    end   = time.time()
    elapsed_time = time.gmtime( end - start )
    elapsed_hour = elapsed_time[3]
    elapsed_min  = elapsed_time[4]
    elapsed_sec  = elapsed_time[5]
    if elapsed_time[2] > 1:
	elapsed_hour += 24
    os.remove(timefile)
    print "%d hour(s) %d minute(s) %d second(s)" % (elapsed_hour, elapsed_min, elapsed_sec)
