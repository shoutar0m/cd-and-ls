# -*- coding: utf-8 -*-
"""My Functions

自作関数モジュールとして .xonshrc から呼び出すクラスを定義します。

Note:
    例えば、.xonshrc で以下のように呼び出します。::

    import sys
    sys.path.append('path/to/myfunc.py')

    from myfunc import CdAndLs
    func = CdAndLs()

"""

import os
import unicodedata
from typing import List


class CdAndLs:
    """Change Directory And List All Components.

    cd した時に ls -a するために必要な属性とメソッドを定義します。

    Attributes:
        new_path (str): 移動先のパスを格納する。
        self.dirs List[str]: ディレクトリ名の一覧を格納する変数。
        self.files List[str]: ファイル名の一覧を格納する変数。
        self.str_len (int): 全角を含んだ文字列の文字数を格納する変数。
        self.dirs_list (str): ディレクトリ一覧を表示するための文字列を格納する変数。
        self.files_list (str): ファイル一覧を表示するための文字列を格納する変数。
        self.dirs_list_header (str): ディレクトリ一覧のタイトル。
        self.files_list_header (str): ファイル一覧のタイトル。

    """

    def __init__(self):
        self.new_path: str = ''
        self.dirs: List[str] = []
        self.files: List[str] = []
        self.str_len: int = 0
        self.dirs_list: str = ''
        self.files_list: str = ''
        self.dirs_list_header: str = '\n' + '------- directories -------'.center(52) + '\n'
        self.files_list_header: str = '\n\n' + '------- files -------'.center(52) + '\n'


    def change_dir(self, path: str) -> None:
        """ディレクトリの移動。

        引数で渡されたディレクトリへ移動し、移動先の絶対パスを取得します。

        Args:
            path (str): 移動先を指定するパス。

        """
        os.chdir(path)
        self.new_path = os.getcwd()

    def get_items(self) -> None:
        """ディレクトリ名とファイル名の取得。

        カレントディレクトリのディレクトリ名とファイル名を全て取得し、アルファベット順にソートします。

        """
        all_items: List[str] = os.listdir(self.new_path)

        dirs: List[str] = [dir_name for dir_name in all_items
                           if os.path.isdir(os.path.join(self.new_path, dir_name))]  # ディレクトリ名のみを取得する。

        files: List[str] = [file_name for file_name in all_items
                            if os.path.isfile(os.path.join(self.new_path, file_name))]  # ファイル名のみを取得する。

        dirs.sort(key=str.lower)
        files.sort(key=str.lower)

        self.dirs, self.files = dirs, files

    def check_japanese_or_not(self, string: str) -> bool:
        """文字列中に日本語が含まれるかの判断。

        引数に渡した文字列に日本語が含まれるか判断します。
        日本語が含まれる場合は、その文字を半角2文字分として文字数をカウントします。

        Args:
            string (str): 日本語が含まれるかどうか判断したい文字列。

        Returns:
            contains_japanese (bool): 全角文字が含まれる場合は True が返されます。

        Note:
            文字列に日本語が含まれるかの判断は、以下のサイトを参考にさせていただきました。
            https://minus9d.hatenablog.com/entry/2015/07/16/231608

        """
        contains_japanese: bool = False
        count: int = 0  # カウンタ変数。

        for char in string:
            name = unicodedata.name(char)

            if ('CJK UNIFIED' in name) or ('HIRAGANA' in name) or ('KATAKANA' in name):
                count = count + 2  # 日本語は2文字としてカウントする。
                contains_japanese = True

            else:
                count = count + 1

        self.str_len = count
        return contains_japanese

    def align_width(self) -> None:
        """ディレクトリ名およびファイル名の文字数を調節。

        各ディレクトリ名およびファイル名に対して、文字数が38文字になるように空白文字を追加します。

        """
        for index, dir_name in enumerate(self.dirs):  # ディレクトリ名について
            
            if self.check_japanese_or_not(dir_name):
                dir_name = dir_name + '/'
                self.dirs[index] = dir_name + ' ' * (38 - self.str_len)  # 日本語が含まれる場合
            else:
                if len(dir_name) >= 28:
                    dir_name = dir_name[:28] + ' ...  '
                dir_name = dir_name + '/'
                self.dirs[index] = dir_name.ljust(38)  # 半角文字のみの場合

        for index, file_name in enumerate(self.files):  # ファイル名について
            if self.check_japanese_or_not(file_name):
                self.files[index] = file_name + ' ' * (38 - self.str_len)  # 日本語が含まれる場合
            else:
                if len(file_name) >= 30:
                    file_name = file_name[:30] + ' ...'
                self.files[index] = file_name.ljust(38)  # 半角文字のみの場合

    def create_display_str(self) -> None:
        """表示する文字列の作成。

        リスト内の各要素を2個ずつ並べて、一覧表示するための文字列を作成します。

        """
        dirs_len, files_len = len(self.dirs), len(self.files)
        dirs_list, files_list, = '', ''  # 作成した文字列を格納する。

        # ディレクトリ名について
        for i in range(0, dirs_len - 1, 2):  # 2個ずつ並べる。
            dirs_list = dirs_list + self.dirs[i] + self.dirs[i + 1] + '\n'

        if self.dirs and (dirs_len % 2):  # 奇数個 (0でない) の場合。
            dirs_list = dirs_list + self.dirs[-1]

        # ファイル名について
        for i in range(0, files_len - 1, 2):  # 2個ずつ並べる。
            files_list = files_list + self.files[i] + self.files[i + 1] + '\n'

        if self.files and (files_len % 2):  # 奇数個 (0でない) の場合。
            files_list = files_list + self.files[-1]

        self.dirs_list, self.files_list = dirs_list, files_list

    def main(self, path):
        """メインメソッド。

        上記で定義したメソッドを適切な順序で呼び出します。
        .xonshrc でこのメソッドを呼び出してください。

        """
        self.change_dir(path)  # 指定したパスへ移動。
        self.get_items()  # ディレクトリ名とファイル名を全て取得。
        self.align_width()  # 幅が半角で38文字分になるように空白を追加。
        self.create_display_str()  # 2列ずつに並べて文字列を作成。

        if not self.dirs_list:
            self.dirs_list = '↪︎ No Directories'  # ディレクトリが無い場合。

        if not self.files_list:
            self.files_list = '↪︎ No files'  # ファイルが無い場合。

        print(self.dirs_list_header + self.dirs_list + self.files_list_header + self.files_list)
