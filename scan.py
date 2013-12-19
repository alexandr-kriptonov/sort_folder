#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import logging.config
from optparse import OptionParser
import sys
from files_to_sort import Files_to_sort


def params():
    parser = OptionParser()
    parser.add_option("-d", "--SCANDIR", dest="SCANDIR",
                      help="Scanned dirrectory", metavar="DIR")
    (options, args) = parser.parse_args()

    if options.SCANDIR:
        SCANDIR = os.path.expanduser(options.SCANDIR)
    else:
        SCANDIR = None

    return SCANDIR

try:
    _log = logging
    _log.config.fileConfig(
        'settings/logging.conf',
        disable_existing_loggers=False)

    _log.info("Start!")
    path_to_scan = params()
    if path_to_scan:
        list_ = Files_to_sort(path_to_scan)
        _log.info("Getting parsed list of files.")
        list_.GetListParsed()
        _log.info("Generated new filenames.")
        list_.generate_filenames()
        _log.info("Moving files.")
        list_.move_files()
        sys.stdout.write("Files in '%s' sorted by types!\n" % (path_to_scan))
        _log.info("Finish!\n")
    else:
        sys.stdout.write("No scan dirrectory!\nPlease use option -h for help\n")
except KeyboardInterrupt:
    sys.stdout.write("Stopped!\n")
    _log.exception("Program aborted by user!\n")
