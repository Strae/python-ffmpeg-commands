#!/usr/local/bin/python

"""
Slice a video reencoding at 25 FPS.
Arguments:
    path of the file
The file must be in the format
sourceFilePath BEGIN END outputName
BEGIN and END should be in format HH:MM:SS
"""

import os, sys, subprocess

def stringToSeconds(string):
    """ Return the number of seconds in a time string in the format HH:MM:SS """
    h, m, s = string.split(':')
    return (int(h) * 3600) + (int(m) * 60) + int(s)

def secondsToString(seconds):
    """ Return a string in the format HH:MM:SS for a given number of seconds """
    if seconds < 60:
        return "00:00:%s" % '{0:02g}'.format(seconds)
    else:
        mins = int(seconds) / 60
        seconds = int(seconds) % 60
        if mins < 60:
            return "00:%s:%s" % ('{0:02g}'.format(mins), '{0:02g}'.format(seconds))
        else:
            hours = mins / 60
            return "%s:%s:%s" % (
                '{0:02g}'.format(hours),
                '{0:02g}'.format(mins % 60),
                '{0:02g}'.format(seconds)
            )

with open(sys.argv[1], 'rb') as data:
    pieces = [line.strip('\n').split(' ') for line in data]
    for piece in pieces:
        try:
            # calculate the time diff in seconds
            outputPath = os.path.join(
                os.path.dirname(piece[0]), ''.join([piece[3], '.mp4']))
            print "Begin with %s" % outputPath
            beginSeconds = stringToSeconds(piece[1])
            endSeconds = stringToSeconds(piece[2])
            # check if the folder exist.
            if not os.path.exists(os.path.dirname(outputPath)):
                os.makedirs(os.path.dirname(outputPath))
            command = ['ffmpeg', '-y', '-i', piece[0], '-ss', ''.join([piece[1], '.0']), '-t',
                ''.join([secondsToString(endSeconds - beginSeconds), '.0']), '-codec:v',
                 'libx264', '-profile:v', 'high', '-preset', 'slower', '-b:v', '707k',
                '-threads 0', '-codec:a', 'aac', '-strict', '-2', '-b:a', '65k', '-r',
                 '25', outputPath, '> /dev/null  2>&1'
            ]
            os.system(' '.join(command))
            print "  done with %s" % outputPath
        except:
            print "Something went wrong with %s" % ' '.join(piece)
