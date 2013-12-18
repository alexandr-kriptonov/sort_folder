#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil


def GetListFile(RootPath):
    ListFiles = []
    for filename in os.listdir(RootPath):
        path = os.path.join(RootPath, filename)
        if not os.path.isdir(path):
            ListFiles.append(path)
        else:
            ListFiles += GetListFile(path)
    return ListFiles


def create_path(path, permission=0777):
    if not os.path.exists(path):
        os.makedirs(path)
        os.chmod(path, permission)
        return 1
    return 2


def move_file(full_start_filename, end_path):

    filename = unicode(os.path.basename(full_start_filename), "utf-8")
    full_end_filename = unicode(os.path.join(end_path, filename))

    create_path(end_path, 0777)

    if os.path.isdir(end_path):
        shutil.move(full_start_filename, full_end_filename)

        if os.path.isfile(full_end_filename):
            return True
        else:
            return False
    else:
        return False
