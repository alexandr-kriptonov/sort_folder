#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from cmagic import CMagic
from utils import filesutils as fsus
from configparser import SafeConfigParser
from shutil import copytree, rmtree
# import logging


home_dir = os.path.expanduser("~")
init_path = "downloads_"
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
    'x-python',
    'plain',
    'png'
]


class GetListFiles:

    def __init__(self, root_path):
        # import pdb; pdb.set_trace
        self.config = SafeConfigParser()
        self.config.read('/home/kripton/Dropbox/scripts/settings/main.ini')
        # self.types = self.config["main"].items()[0][1].split(",")
        self.types = types
        self.root_path = root_path

    def GetListParsed(self, mode=None):
        InpuList = fsus.GetListFile(self.root_path)
        # print type(InpuList)
        Result = {}
        Result["other"] = []
        if mode:
            # Result["other"] = InpuList
            # return Result
            pass
        else:
            for i, item in enumerate(InpuList):
                temp_file = CMagic(item)
                __type = None
                for _type in self.types:
                    if temp_file.is_(_type):
                        __type = _type
                        break

                pop_item = InpuList.pop(i)
                if __type:
                    if not __type in Result:
                        Result[__type] = []
                    Result[__type].append(pop_item)
                else:
                    Result["other"].append(pop_item)

        return Result

    def MoveFiles(self, list_files):

        for block in list_files:
            for filename in list_files[block]:
                fsus.move_file(filename, os.path.join(end_path, block))

    # def ReturnFiles():


list_ = GetListFiles(path_to_scan)
# import debug
list__ = list_.GetListParsed()
import debug
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
