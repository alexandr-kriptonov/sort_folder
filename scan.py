#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import logging.config
import sys
from files_to_sort import Files_to_sort
# import logging


home_dir = os.path.expanduser("~")
init_path = "downloads_"
path_to_scan = os.path.join(home_dir, init_path)

try:
    _log = logging
    _log.config.fileConfig(
        'settings/logging.conf',
        disable_existing_loggers=False)

    _log.info("Start!")
    list_ = Files_to_sort(path_to_scan)
    _log.info("Getting parsed list of files.")
    list_.GetListParsed()
    _log.info("Generated new filenames.")
    list_.generate_filenames()
    _log.info("Moving files.")
    list_.move_files()
    sys.stdout.write("Files in '%s' sorted by types!\n" % (path_to_scan))
    _log.info("Finish!\n")
except KeyboardInterrupt:
    sys.stdout.write("Stopped!\n")
    _log.exception("Program aborted by user!\n")
