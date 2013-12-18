#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from cmagic import CMagic
from utils import filesutils as fsus
from configparser import SafeConfigParser
import logging
import logging.config
import os.path as _path
import progressbar
from progressbar import ETA, Bar
# import logging
__log = []
_log = logging
_log.config.fileConfig(
    'settings/logging.conf',
    disable_existing_loggers=False
)

home_dir = os.path.expanduser("~")
init_path = "_music"
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
    'png',
    'mp3'
]


class GetListFiles:

    def __init__(self, root_path):
        # import pdb; pdb.set_trace
        self.config = SafeConfigParser()
        self.config.read('/home/kripton/Dropbox/scripts/settings/main.ini')
        # self.types = self.config["main"].items()[0][1].split(",")
        self.types = types
        self.root_path = root_path
        self.log = []

    def GetListParsed(self, FileList=None):
        #  list of files in input dirrectory
        if not FileList:
            FileList = fsus.GetListFile(self.root_path)
        init_len = len(FileList)
        v = float(100)/float(init_len)
        value = v
        bar = progressbar.ProgressBar(
            maxval=100.0,
            widgets=['Getting filenames ', Bar('>'), ' ', ETA(), ]).start()
        Result = {}
        Result["other"] = []

        def get_type(current_file):
            for _type in self.types:
                if current_file.is_(_type):
                    return _type
            return "other"

        while len(FileList):
            head_item = FileList[0]
            current_file = CMagic(head_item)
            type_item = get_type(current_file)
            pop_item = FileList.pop(0)
            if type_item:
                if not type_item in Result:
                    Result[type_item] = []
                Result[type_item].append(pop_item)
            else:
                Result["other"].append(pop_item)
            value += v
            if value > 100.0:
                value = 100.0
            bar.update(value)
        bar.finish()

        self.l_filenames_parsed = Result

    def generate_filenames(self, lfp=None):
        if not lfp:
            lfp = self.l_filenames_parsed
        init_len = len(lfp)
        v = float(100)/float(init_len)
        value = v
        bar = progressbar.ProgressBar(
            maxval=100.0,
            widgets=['Generate new filenames ', Bar('>'), ' ', ETA(), ]).start()
        result_list = {}
        count = 0
        # import pdb; pdb.set_trace()
        for _type in lfp:
            current_list = lfp[_type]
            # import pdb; pdb.set_trace()
            for init_file in current_list:
                # import pdb; pdb.set_trace()
                _dirname = _path.dirname(init_file)
                final_dir = _path.join(_dirname, _type)
                result_list[count] = {}
                result_list[count]["init_file"] = init_file
                result_list[count]["final_dir"] = final_dir
                count += 1
                value += v
                if value > 100.0:
                    value = 100.0
                bar.update(value)
        self.filename_to_move = result_list
        bar.finish()

    def move_files(self, list_files=None):
        if not list_files:
            list_files = self.filename_to_move
        init_len = len(list_files)
        v = float(100)/float(init_len)
        value = v
        bar = progressbar.ProgressBar(
            maxval=100.0,
            widgets=['Moving files ', Bar('>'), ' ', ETA(), ]).start()
        for i in list_files:
            current_item = list_files[i]
            # import pdb; pdb.set_trace()
            if _path.dirname(current_item["init_file"]) == current_item["final_dir"]:
                continue
            else:
                fsus.move_file(
                    current_item["init_file"], current_item["final_dir"])
            value += v
            if value > 100.0:
                value = 100.0
            bar.update(v)
        bar.finish()

list_ = GetListFiles(path_to_scan)
list_.GetListParsed()
list_.generate_filenames()
list_.move_files()

(source, destination) = (end_path, path_to_scan)
print "source: %s" % (path_to_scan)
