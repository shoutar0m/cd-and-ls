# -*- coding: utf-8 -*-
"""My Functions

自作関数として .xonshrc から呼び出すクラスを定義します。

Note:
    例えば、.xonshrc で以下のように呼び出します。::

    import sys
    sys.path.append('path/to/myfunc.py')

    from myfunc import CdAndLs
    func = CdAndLs()

"""

import os


class CdAndLs:
    """Change Directory And List All Components.

    cd した時に ls -a するために必要な属性とメソッドを定義します。

    Attributes:
        new_path (str): 移動先のパスを格納する。
        self.dirs List[str]: ディレクトリ名の一覧を格納する変数。
        self.files List[str]: ファイル名の一覧を格納する変数。
        self.str_len (int): 全角を含んだ文字列の文字数を格納する変数。
        self.dirs_list_header (str): ディレクトリ一覧のタイトル。
        self.files_list_header (str): ファイル一覧のタイトル。
        self.dirs_list_body (str): ディレクトリ一覧を表示するための文字列を格納する変数。
        self.files_list_body (str): ファイル一覧を表示するための文字列を格納する変数。

    """

    def __init__(self):
        self.new_path: str = ''
        self.dirs: list[str] = []
        self.files: list[str] = []
        self.str_len: int = 0
        self.dirs_list_header: str = '\n' + '------- directories -------'.center(55) + '\n'
        self.files_list_header: str = '\n\n' + '------- files -------'.center(55) + '\n'
        self.dirs_list_body: str = ''
        self.files_list_body: str = ''


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
        all_items: list[str] = os.listdir(self.new_path)

        dirs: list[str] = [dir_name for dir_name in all_items
                           if os.path.isdir(os.path.join(self.new_path, dir_name))]  # ディレクトリ名のみを取得する。

        files: list[str] = [file_name for file_name in all_items
                            if os.path.isfile(os.path.join(self.new_path, file_name))]  # ファイル名のみを取得する。

        dirs.sort(key=str.lower)
        files.sort(key=str.lower)

        self.dirs, self.files = dirs, files

    def align_width(self, string: str, is_dir_name: bool = True) -> bool:
        """文字幅を考慮して文字数を42文字に整える。

        引数に渡した文字列の1文字毎の文字幅を考慮しながら文字列の長さを42文字に整えます。
        日本語が含まれる場合は、その文字を半角2文字分としてカウントします。

        Args:
            string (str): 日本語が含まれるかどうか判断したい文字列。
            is_dir_name (bool): ディレクトリ名かどうかを表す真偽値。

        Returns:
            return_string (str): 半角30文字分を超える長さの場合は途中で文字列を返します。

        """
        width: int = 0
        return_string: str = ''

        for i in range(len(string)):
            return_string = return_string + string[i]

            if string[i].isascii():
                width = width + 1
            elif string[i] in ('゙', '゚'):
                width = width + 0  # 濁点などは0文字分としてカウントする。
            else:
                width = width + 2  # 日本語は半角2文字分としてカウントする。
            
            if width>=30:
                if string[i+1] in ('゙', '゚'):
                    return_string = return_string + string[i+1]
                return_string = return_string + '... '
                if is_dir_name:
                    return_string = return_string + '/'
                    return_string = return_string + ' ' * (42 - (width+len('... /')))
                else:
                    return_string = return_string + ' ' * (42 - (width+len('... ')))
                break
        else:
            if is_dir_name:
                return_string = return_string + '/'
                return_string = return_string + ' ' * (41 - width)
            else:
                return_string = return_string + ' ' * (42 - width)

        return return_string

    def change_names(self) -> None:
        """ディレクトリ名およびファイル名変更。

        各ディレクトリ名およびファイル名をalign_width()メソッドを使用して変更する。

        """
        for index, dir_name in enumerate(self.dirs):  # ディレクトリ名について
            self.dirs[index] = self.align_width(dir_name, is_dir_name=True)

        for index, file_name in enumerate(self.files):  # ファイル名について
            self.files[index] = self.align_width(file_name, is_dir_name=False)

    def set_each_list_body(self) -> None:
        """表示する文字列の作成。

        リスト内の各要素を2個ずつ並べて、一覧表示するための文字列を作成します。

        """
        dirs_len, files_len = len(self.dirs), len(self.files)
        dirs_list_body, files_list_body, = '', ''  # 作成した文字列を格納する。

        # ディレクトリ名について
        for i in range(0, dirs_len - 1, 2):  # 2個ずつ並べる。
            dirs_list_body = dirs_list_body + self.dirs[i] + self.dirs[i + 1] + '\n'

        if self.dirs and (dirs_len % 2):  # 奇数個 (0でない) の場合。
            dirs_list_body = dirs_list_body + self.dirs[-1]

        # ファイル名について
        for i in range(0, files_len - 1, 2):  # 2個ずつ並べる。
            files_list_body = files_list_body + self.files[i] + self.files[i + 1] + '\n'

        if self.files and (files_len % 2):  # 奇数個 (0でない) の場合。
            files_list_body = files_list_body + self.files[-1]

        self.dirs_list_body, self.files_list_body = dirs_list_body, files_list_body

    def main(self, path):
        """メインメソッド。

        上記で定義したメソッドを適切な順序で呼び出します。
        .xonshrc でこのメソッドを呼び出してください。

        """
        self.change_dir(path)  # 指定したパスへ移動。
        self.get_items()  # ディレクトリ名とファイル名を全て取得。
        self.change_names()  # 幅が半角で42文字分になるように空白を追加。
        self.set_each_list_body()  # 2列ずつに並べて文字列を作成。

        if not self.dirs_list_body:
            self.dirs_list_body = '↪︎ No Directories'  # ディレクトリが無い場合。

        if not self.files_list_body:
            self.files_list_body = '↪︎ No files'  # ファイルが無い場合。

        print(self.dirs_list_header + self.dirs_list_body + self.files_list_header + self.files_list_body)
