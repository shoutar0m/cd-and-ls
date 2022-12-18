# Change Directory AND LiSt all components
![demo](./imgs/demo.png)
**cd** (ディレクトリを移動) した後に **ls -a** (移動先のディレクトリ名・ファイル名を全て表示) も実行する [xonsh](https://xon.sh) 用の関数を作成しました。  


## Requirements
- Python>=3.10.5
- xonsh>=0.13.3

## Usage
1.  以下のコマンドでこのリポジトリをクローンしてください。

	```
	git clone "https://github.com/shoutar0m/cd-and-ls"
	```

2. `.xonshrc` を適切なディレクトリに作成してください。
3. 以下のコードや `.xonshrc_example` を参考に、`CdAndLs` クラスの `main()` メソッドを呼び出すコードとエイリアスを `.xonshrc` に追記してください。

	```.xonshrc
	import sys
	sys.path.append('path/to/myfunc.py')
		
	from myfunc import CdAndLs
		
	# 自作関数の定義
	def cd_and_ls(arg):
		
	    ︙
		
	    func = CdAndLs()
	    func.main(path)
		
	    ︙
		
		
	# エイリアスの作成
	aliases['cd'] = cd_and_ls
	```

3. ターミナルアプリを起動し、以下のように `cd` コマンドをご使用ください。

	```
	cd Development/Python/xonsh_func  # Example
	```

![demo](./imgs/demo.png)

