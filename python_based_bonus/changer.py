#!/usr/bin/env python3
import sys
import os
import time
import random
from subprocess import check_call

def main(argv):
    it_just_started = True
    change_cmd_tmlt = ["/usr/bin/env", "dconf", "write", "/org/mate/desktop/background/picture-filename"] #'/home/y/Pictures/wallpaper/IMG_0147.JPG'"
    folder_with_wp = argv[1]
    debug = __debug__#True if ("-d") in argv else False
    if debug:
                print ("Debug mode is on")
    if ("M" in argv[2]):
        chage_interval = int(argv[2][:-1])*60
    elif ("H" in argv[2]):
        chage_interval = (int(argv[2][:-1])*60)*60
    else:
        chage_interval = int(argv[2])
    files = [x for x in os.listdir(folder_with_wp) if ("jpg" in x.lower())]
    poll_files = list()
    try:
        while True:
            print ("Press Ctrl + C to stop")
            files_at_the_moment = [x for x in os.listdir(folder_with_wp) if ("jpg" in x.lower())]
            files_diff = set(files_at_the_moment) - set(files)
            if len(files_diff) > 0:
                print ("Found file(s): %s" % ", ".join(files_diff))
                files.extend(files_diff)
            if len(poll_files) == 0:
                if not it_just_started:
                    print ("One ring complete!")
                poll_files = files[:]
            print ("left to show: %s" % len(poll_files))
            index = random.randint(0, len(poll_files)-1)
            if not it_just_started:
                time.sleep(chage_interval)
            change_cmd = change_cmd_tmlt[:]
            choosed = os.path.join(folder_with_wp, poll_files.pop(index))
            change_cmd.append("'%s'" % (choosed))
            if debug:
                                print (change_cmd)
            check_call(change_cmd)
            it_just_started = False
            
    except KeyboardInterrupt:
        return 0
    return 1

if (__name__ == "__main__"):
    if len(sys.argv) != 3:
        print ("Using: changer.py <path to folder with walpappers> <time(|M|H)>\n"
                       + "       e.g. ./changer.py /path/to/wallpapers 10 -- 1 per 10 sec\n"
                       + "       e.g. ./changer.py /path/to/wallpapers 1M -- 1 per 1 min\n")
    else:
        sys.exit(main(sys.argv))
