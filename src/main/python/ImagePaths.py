'''
ImagesPaths.py

Copyright © 2019 Hashidzume Hikaru. All rights reserved.
Released under the GPL license.
'''

import os
from PyQt5 import QtCore

class ImagePaths( QtCore.QObject ):

    def __init__(self):
        super().__init__()

        self.__path_list = [] # 読み取り専用
        self.__dir_path = "" # 読み取り専用

    # 添字アクセル可能にするためのメソッド
    def __getitem__(self, key):
        return self.__path_list[key]

    # イテレート可能にするためのメソッド
    def __iter__(self):
        self.__itr_current = 0
        return self

    def __next__(self):
        if self.__itr_current == len(self.__path_list):
            raise StopIteration()

        ret = self.__path_list[self.__itr_current]
        self.__itr_current += 1
        return ret

    # ifぶんでTrue/Falseを判定できるようにする
    def __bool__(self):
        return bool(self.__path_list)

    # len()で長さを所得できるようにする
    def __len__(self):
        return len(self.__path_list)

    def get_dir_path(self) -> str:
        return self.__dir_path

    def make_list(self, dir_path: str) -> None:

        # ディレクトリのパスを保存
        self.__dir_path = dir_path

        # __path_listに先に入っていたら消す
        if self.__path_list:
            self.__path_list.clear()

        # dir_path以下のファイルの名前を所得
        tmp_file_list = os.listdir(dir_path)

        # サポートする拡張子のファイルだけself.__path_listに追加
        valid_extensions = ['.JPG', '.JPEG', '.PNG', '.GIF'] # 拡張子の頻出順にすることで高速化を期待
        for file in tmp_file_list:
            for valid_extension in valid_extensions:
                extension = os.path.splitext(file) # 拡張子以外と拡張子に分ける

                if valid_extension == extension[1].upper():
                    self.__path_list.append(dir_path + os.sep + file)
                    break