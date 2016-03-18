#!/usr/local/bin/python

"""
Apply fadein and fadeout effects to all the video present in a directory.
Arguments:
    folder path
    fadein duration in seconds (optional, defaul 1s)
    fadeout duration in seconds (optional, default 1s)
"""

import os, sys, glob, subprocess
from hachoir_core.cmd_line import unicodeFilename
from hachoir_metadata import extractMetadata
from hachoir_parser import createParser

FPS = 25

path = sys.argv[1]
destinationPath = os.path.join(path, 'faded')
try:
    if not os.path.exists(destinationPath):
        os.mkdir(destinationPath)
except:
    print "Unable to create output folder."
    exit()

try:
    fadeInDuration = int(sys.argv[2])
except IndexError:
    fadeInDuration = 1

try:
    fadeOutDuration = int(sys.argv[3])
except IndexError:
    fadeOutDuration = 1

if 0 >= fadeOutDuration and 0 >= fadeInDuration:
    raise ValueError('WTF IM SUPPOSED TO FADE?')

for filePath in glob.glob(''.join([path, '/*.mp4'])):
    try:
        print "Begin with %s" % filePath
        # Get file lenght and framerate
        duration = extractMetadata(createParser(unicodeFilename(filePath))).get('duration').seconds
        outputPath = os.path.join(
            destinationPath,
            os.path.basename(filePath)
        )

        videoFadeCmd = []
        audioFadeCmd = []
        if 0 < fadeInDuration:
            videoFadeCmd.append("fade=in:0:%s" % (fadeInDuration * FPS))
            audioFadeCmd.append("afade=t=in:ss=0:d=%s" % fadeInDuration)
        if 0 < fadeOutDuration:
            fadeOutDelta = duration - fadeOutDuration
            videoFadeCmd.append("fade=out:%s:%s" % ((fadeOutDelta * FPS), fadeOutDuration * FPS))
            audioFadeCmd.append("afade=t=out:st=%s:d=%s" % (fadeOutDelta, fadeOutDuration))

        videoFadeString = "'%s'" % ','.join(videoFadeCmd)
        audioFadeString = "'%s'" % ','.join(audioFadeCmd)

        command = [
            'ffmpeg', '-y', '-i', filePath, '-async', '1', '-strict', '-2', '-vf',
            videoFadeString, '-af', audioFadeString, outputPath, '> /dev/null  2>&1'
        ]
        os.system(' '.join(command))
        print "  done with %s > %s" % (filePath, outputPath)
    except ValueError:
        print "%s doesnt have a required value." % filePath
    except:
        print "Somethig went wrong."
