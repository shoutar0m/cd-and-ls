import unicodedata
import os


class CdAndLs:

    def __init__(self):
        self.new_path = ""  # 移動先のパスを格納する。
        self.dirs = []
        self.files = []
        self.dir_title = "\n" + "------- directories -------".center(52) + "\n"
        self.files_title = "\n\n" + "------- files -------".center(52) + "\n"
        self.dirs_list = ""  # ディレクトリ名の一覧表示を格納する変数
        self.files_list = ""  # ファイル名の一覧表示を格納する変数
        self.str_len = 0  # 全角を含んだ文字列の文字数を格納する。

    def change_dir(self, path):
        """ 引数で渡されたディレクトリへ移動し、移動先の絶対パスを取得するメソッド """

        # 作業ディレクトリを移動する。
        os.chdir(path)

        # 移動した先のパスを取得する。
        self.new_path = os.getcwd()

    def get_items(self):
        """ カレントディレクトリのディレクトリ名とファイル名を全て取得し、アルファベット順にソートするメソッド """

        # カレントディレクトリのディレクトリ名とファイル名を全て取得する。
        all_items = os.listdir(self.new_path)  # 全てを取得する。
        dirs = [dir_name for dir_name in all_items \
          if os.path.isdir(os.path.join(self.new_path, dir_name))]  # ディレクトリ名のみを取得する。
        files = [file_name for file_name in all_items \
          if os.path.isfile(os.path.join(self.new_path, file_name))]  # ファイル名のみを取得する。

        # アルファベット順にソートする。
        dirs.sort(key=str.lower)  # ディレクタ名
        files.sort(key=str.lower)  # ファイル名

        self.dirs = dirs
        self.files = files

    def is_fullwidth(self, string):
        """ 引数に渡した文字列に全角が含まれるか判断して文字数をカウントするメソッド """

        fullwidth = False  # 全角が含まれるかどうか。
        count = 0  # カウンタ変数を初期化する。

        for char in string:
            name = unicodedata.name(char)

            if "CJK UNIFIED" in name \  # 「漢字」「ひらがな」「カタカナ」のいずれかが含まれているか
                    or "HIRAGANA" in name \
                    or "KATAKANA" in name:
                count = count + 2  # 全角文字は2文字としてカウントする。
                fullwidth = True

            else:
                count = count + 1

        self.str_len = count
        return fullwidth

    def add_blank(self):
        """ リストの各要素に対して、文字数が38文字になるように空白文字を追加するメソッド """

        # ディレクトリ名について
        for index, dir_name in enumerate(self.dirs):
            dir_name = dir_name + "/"
            if self.is_fullwidth(dir_name):
                self.dirs[index] = dir_name + " " * (38 - self.str_len)  # 全角文字が含まれる場合
            else:
                self.dirs[index] = dir_name.ljust(38)  # 半角文字のみの場合

        # ファイル名について
        for index, file_name in enumerate(self.files):
            if self.is_fullwidth(file_name):
                self.files[index] = file_name + " " * (38 - self.str_len)  # 全角文字が含まれる場合
            else:
                self.files[index] = file_name.ljust(38)  # 半角文字のみの場合

    def arrange_list(self):
        """ リスト内の各要素を2個ずつ並べて一覧表示になるように整形する。 """

        dis_len = len(self.dirs)
        files_len = len(self.files)

        dirs_list = ""  # 整形した文字列を格納する。(ディレクトリ名)
        files_list = ""  # 整形した文字列を格納する。(ファイル名)

        # ディレクトリ名について
        for i in range(0, dis_len - 1, 2):  # 2個ずつ並べる。
            dirs_list = dirs_list + self.dirs[i] + self.dirs[i + 1] + "\n"

        if self.dirs and (dis_len % 2):  # 奇数個(0でない)の場合
            dirs_list = dirs_list + self.dirs[-1]

        self.dirs_list = dirs_list

        # ファイル名について
        for i in range(0, files_len - 1, 2):  # 2個ずつ並べる。
            files_list = files_list + self.files[i] + self.files[i + 1] + "\n"

        if self.files and (files_len % 2):  # 奇数個(0でない)の場合
            files_list = files_list + self.files[-1]

        self.files_list = files_list
