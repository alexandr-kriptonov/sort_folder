# -*- coding: utf-8 -*-

from cmagic import CMagic
from utils import filesutils as fsus
import logging
import os.path as _path
from utils import progressbar
from utils.progressbar import ETA, Bar
import sys

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


class Files_to_sort(object):

    def __init__(self, root_path):
        self.types = types
        self.root_path = root_path
        self.l_filenames_parsed = None
        self.filename_to_move = None
        self._log = logging.getLogger(__name__)

    def GetListParsed(self, FileList=None):
        #  list of files in input dirrectory
        if not FileList:
            FileList = fsus.get_list_files(self.root_path)
        init_len = len(FileList)
        v = float(100)/float(init_len)
        value = v
        bar = progressbar.ProgressBar(
            maxval=100.0,
            widgets=['Getting filenames      ', Bar('>'), ' ', ETA(), ]).start()
        Result = {}
        Result["other"] = []

        def get_type(current_file):
            for _type in self.types:
                if current_file.is_(_type):
                    return _type
            return "other"

        count = 0
        while len(FileList):
            count += 1
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
        sys.stdout.write("Find: %s files\n" % count)

        self.l_filenames_parsed = Result
        self._log.info("parsed list: %s" % self.l_filenames_parsed)

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
        for _type in lfp:
            current_list = lfp[_type]
            for init_file in current_list:
                _dirname = _path.dirname(init_file)
                if _path.join(self.root_path, _type) == _dirname:
                    final_dir = "not_move"
                else:
                    final_dir = _path.join(self.root_path, _type)
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
        sys.stdout.write("New filenames list generated!\n")
        self._log.info("New filenames list: %s" % self.filename_to_move)

    def move_files(self, list_files=None):
        if not list_files:
            list_files = self.filename_to_move
        init_len = len(list_files)
        v = float(100)/float(init_len)
        value = v
        bar = progressbar.ProgressBar(
            maxval=100.0,
            widgets=['Moving files           ', Bar('>'), ' ', ETA(), ]).start()
        count = 0
        for i in list_files:
            current_item = list_files[i]
            if current_item["final_dir"] == "not_move":
                continue
            else:
                try:
                    response_move = fsus.move_file(
                        current_item["init_file"], current_item["final_dir"])
                    if response_move:
                        count += 1
                except Exception, e:
                    self._log.exception(e.message)
            value += v
            if value > 100.0:
                value = 100.0
            bar.update(v)
        bar.finish()
        sys.stdout.write("Moved %s files\n" % count)
        self._log.info("Moved %s files" % count)
