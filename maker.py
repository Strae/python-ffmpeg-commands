#!/usr/local/bin/python

"""
Add the intro movie to all the files inside a specific folder using mmcat
Arguments:
    path of the folder containings all the videos
"""

import os, sys, subprocess
from glob import glob

# Temp data
TMP_PATH = '/tmp'
# Gingle fullpath
GINGLE = '/tmp/gingle.mp4'

try:
    path = sys.argv[1]
except IndexError:
    print "Missing folder name."
    exit()

for filePath in glob(''.join([path, '/*.mp4'])):
    try:
        print "Begin with %s" % filePath
        outputPath = os.path.join(TMP_PATH, os.path.basename(filePath))
        command = ' '.join(['mmcat', GINGLE, filePath, outputPath, '> /dev/null  2>&1'])
        os.system(command)
        print "  done with %s > %s" % (filePath, outputPath)
    except:
        print "Error."
print "Finish."
exit()
