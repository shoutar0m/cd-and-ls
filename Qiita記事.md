---
title: 【Python】xonsh で cd した時に ls してくれる関数
tags: Python xonsh シェルコマンド
author: shoutar0m
slide: false
---
# 0. はじめに

初投稿となります。間違っているところや、説明が不十分なところがありましたら、ご指摘いただけると大変嬉しいです。

# 1. きっかけ

私は以前、シェルは zsh を使っていました。その時、[こちら](https://qiita.com/k941226/items/e0b9a4fa06bab275f96b)の記事を参考に「cd した時に ls してくれる関数」を .zshrc に記述し使用していました。 
ある時、[こちら](https://qiita.com/yoidea/items/61ac5356b63437963382)の記事などから、Python で動くという非常に魅力的なシェル「xonsh」の存在を知り、すぐに導入しました。(この時同時に Hyper も知り、かっこいいなぁと思い導入しました。)
xonsh では、Python で作成した自作関数をシェルコマンドとして使用できるので、**自分オリジナルの「cd した時に ls してくれる関数」**を作ってみることにしました。

# 2. 「cd した時に ls してくれる関数」で使用するクラスを作成する

「ls で一覧表示する際にはディレクトリ名・ファイル名を2列に揃えて並べたい」、「ディレクトリ名とファイル名は分けて並べたい」など、こだわりが多かったので、それらのこだわりを実現するためのクラスを別ファイルで定義し、.xonshrc からそれらを呼び出すことにしました。

:::note info
以下のコードは抜粋版です。完全版は GitHub で公開しています。
:::

https://github.com/shoutar0m/cd-and-ls

```myfunc.py
import os
import unicodedata
from typing import List


class CdAndLs:
    """Change Directory AND LiSt all components.

    cd した時に ls -a するために必要な属性とメソッドを定義します。

    Attributes:
        self.dir_title (str): ディレクトリ一覧のタイトル。
        self.files_title (str): ファイル一覧のタイトル。
        new_path (str): 移動先のパスを格納する。
        self.dirs List[str]: ディレクトリ名の一覧を格納する変数。
        self.files List[str]: ファイル名の一覧を格納する変数。
        self.str_len (int): 全角を含んだ文字列の文字数を格納する変数。
        self.dirs_list (str): ディレクトリ一覧を表示するための文字列を格納する変数。
        self.files_list (str): ファイル一覧を表示するための文字列を格納する変数。
    """

    def __init__(self):
        self.dir_title: str = '\n' + '------- directories -------'.center(52) + '\n'
        self.files_title: str = '\n\n' + '------- files -------'.center(52) + '\n'
        self.new_path: str = ''
        self.dirs: List[str] = []
        self.files: List[str] = []
        self.str_len: int = 0
        self.dirs_list: str = ''
        self.files_list: str = ''

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
        ︙

    def japanese_contains_judge(self, string: str) -> bool:
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
        ︙

    def align_width(self) -> None:
        """ディレクトリ名およびファイル名の文字数を調節。

        各ディレクトリ名およびファイル名に対して、文字数が38文字になるように空白文字を追加します。
        """
        ︙

    def create_display_str(self) -> None:
        """表示する文字列の作成。

        リスト内の各要素を2個ずつ並べて、一覧表示するための文字列を作成します。
        """
        ︙

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

        print(self.dir_title + self.dirs_list + self.files_title + self.files_list)

```

# 3. 「cd した時に ls してくれる関数」を作成する
上記のクラスをもとに、目的の関数を .xonshrc に記述していきます。

まずはじめに、作成した myfunc.py へのパスを追加し、`CdAndLs` をインポートします。

```~/.xonshrc
# 自作関数の定義
import sys
sys.path.append("myfunc.pyが保存されているディレクトリまでのパス")

from myfunc import CdAndLs
```

次に、目的の関数である**「cd した時に ls してくれる関数」**を定義します。

```~/.xonshrc
# 自作関数の作成
def cd_and_ls(arg):
    """cd した時に ls してくれる関数。"""

    try:
        if arg[:1]:
            path = str(arg[:1][0])
        else:
            path = 'path/to/home'  # cd のみ (引数無し) の場合

        func = CdAndLs()
        func.main(path)

    except FileNotFoundError:
        print(f'\nNo such directory: "{path}"')
```

この関数が呼び出されると、

- 引数として移動先までのパスが渡された場合はそのパスを、何も渡されなかった場合はホームディレクトリまでのパスを、 変数 `path` に格納する。
- `CdAndLs` の `main()` メソッドに変数 `path` が渡されます。
- `CdAndLs` の `main()` メソッド内で `change_dir()` が呼び出されます。ここで指定されたパスへ移動します。
- `get_items()` で移動先のディレクトリ名とファイル名を全て取得します。
- `align_width()` で取得したディレクトリ名とファイル名に `' '` を付け足して文字数を38文字に揃えます。
- `create_display_str()` で一覧表示するために2列ずつに並べて文字列を作成します。
- 最後に、タイトルと合わせてディレクトリ名一覧・ファイル名一覧を表示します。

という流れで処理が実行されます。
また、例外処理として渡されたパスが存在しなかった場合は、`No such directory: ...` と表示されるようにしています。

最後に、作成した関数 `cd_and_ls` を `cd`という名前で実行できるようにします。

```~/.xonshrc
# エイリアスの作成
aliases["cd"] = cd_and_ls
```

実際に使用するとこのようになります。
　　![スクリーンショット 2021-08-10 21.50.32.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1196928/1c33c801-1879-c2e1-c396-1e3a462602cf.png)

# おわりに
初投稿ということで意気込んでしまい、かなり長文になってしまいました。
最後まで読んでいただきありがとうございました。

# 参考にした記事
1. [zsh導入方法（.zshrcカスタマイズ付き）](https://qiita.com/k941226/items/e0b9a4fa06bab275f96b)
2. [XonshとHyperを勢いで導入した話](https://qiita.com/yoidea/items/61ac5356b63437963382)
3. [Pythonでファイル名・ディレクトリ名の一覧をリストで取得](https://note.nkmk.me/python-listdir-isfile-isdir/)
4. [Pythonで、文字列に日本語が含まれているか判定する](https://minus9d.hatenablog.com/entry/2015/07/16/231608)
5. [Xonshでコマンドを作る](https://qiita.com/riktor/items/2f18db475dc5b2c8d829)
6. [【Python】自作モジュールへのパスの通し方](https://qiita.com/derodero24/items/6e2d809ceb6360211bd2)
