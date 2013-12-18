#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from cmagic import CMagic
from utils import filesutils as fsus
from configparser import SafeConfigParser
from shutil import copytree, rmtree
# import logging


home_dir = os.path.expanduser("~")
init_path = "recup_dir"
path_to_scan = os.path.join(home_dir, init_path)
end_path = os.path.join(home_dir, init_path + "_out")
fsus.create_path(end_path)

types = [
    'bittorrent',
    'mpeg',
    'other',
    'zip',
    'pdf',
    'vnd.djvu',
    'doc',
    'jpeg',
    'rtf',
]


class GetListFiles:

    def __init__(self, root_path):
        import pdb; pdb.set_trace
        self.config = SafeConfigParser()
        self.config.read('/home/kripton/Dropbox/scripts/settings/main.ini')
        # self.types = self.config["main"].items()[0][1].split(",")
        self.types = types
        self.root_path = root_path

    def GetListParsed(self, mode=None):
        InpuList = fsus.GetListFile(self.root_path)
        Result = {}

        if mode:
            Result["other"] = InpuList
            return Result

        for _type in self.types:
            Result[_type] = []

        for _type in self.types:
            for item in InpuList:
                temp_file = CMagic(item)
                # print "<---> %s <---> %s" % (temp_file.getType(),_type)
                # import pdb; pdb.set_trace()
                if temp_file.is_(_type):
                    Result[_type].append(item)
            # Result["all"] = InpuList
        return Result

    def MoveFiles(self, list_files):

        for block in list_files:
            for filename in list_files[block]:
                fsus.move_file(filename, os.path.join(end_path, block))

    # def ReturnFiles():


list_ = GetListFiles(path_to_scan)
list__ = list_.GetListParsed()
list_.MoveFiles(list__)
list__ = list_.GetListParsed("other")
list_.MoveFiles(list__)

# def _logpath(path, names):
#     logging.info('Working in %s' % path)
#     return []   # nothing will be ignored

(source, destination) = (end_path, path_to_scan)
print "source: %s" % (path_to_scan)

rmtree(path_to_scan)
copytree(source, destination)
rmtree(end_path)
