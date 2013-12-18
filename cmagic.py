#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ctypes


class CMagic:
    __mgc = None
    __cookie = None

    def __init__(self, filename):
        #Загружаем libmagic.so
        self.__mgc = ctypes.cdll.LoadLibrary("libmagic.so.1")
        #Создаем новый cookie (требуется для
        #работы с magic-последовательностями)
        #0x10 | 0x400 = MAGIC_MIME (константа
        #декларируется в magic.h)
        self.__cookie = self.__mgc.magic_open(0x10 | 0x400)
        #Загружаем в __cookie
        #/etc/file/magic.mime (т.к. указано None)
        self.__mgc.magic_load(self.__cookie, None)
        self.filename = filename

    def __del__(self):
        #Закрываем __cookie
        self.__mgc.magic_close(self.__cookie)

    def getMType(self):
        #Получаем информацию о файле
        result = self.__mgc.magic_file(self.__cookie, self.filename)
        #magic_file возвращает const char*,
        #mimetype.value - это строка по указателю
        mimetype = ctypes.c_char_p(result)
        rez = mimetype.value
        return rez

    def getType(self):
        self.mime = self.getMType()
        return self.mime

    def is_torrent(self):
        self.getType()
        if self.mime.count("bittorrent"):
            return 1
        return 0

    def is_mpeg(self):
        self.getType()
        if self.mime.count("mpeg"):
            return 1
        return 0

    def is_(self, _type):
        self.getType()
        if self.mime.count(_type):
            return 1
        return 0
