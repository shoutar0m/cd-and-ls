# Change Directory AND LiSt All components
![demo](./imgs/demo.png)
I created a useful function that functions on xonsh.  
If the `cd` (**Change Directory**) command was called on a terminal in which this function is applied, this function calls the `ls -a` (**LiSt All components**) command together, so the working directory is moved to and then the terminal shows what directories and files are in that.  
(This functions correctly only in **English** or **Japanese** environment.)

## Requirements
- Python>=3.10.5
- xonsh>=0.13.3

## How to use
1.  Clone this repository by the following command.

	```
	git clone "https://github.com/shoutar0m/cd-and-ls"
	```

2. Create `.xonshrc` in any directory.
3. Add some source codes to call the `main()` method in the `CdAndLs` class and declare an alias to make this function the `cd` command. you can see the following source codes and `.xonshrc_example` as a sample.

	```.xonshrc
	import sys
	sys.path.append('path/to/myfunc.py')
		
	from myfunc import CdAndLs
		
	# Declare my function.
	def cd_and_ls(arg):
		
	    ︙
		
	    func = CdAndLs()
	    func.main(path)
		
	    ︙
		
		
	# Declare an alias.
	aliases['cd'] = cd_and_ls
	```

3. Launch your terminal and try the `cd` command like the following. 

	```
	cd Development/Python/xonsh_func  # Example
	```
	
	Your terminal must show the following chart.
![demo](./imgs/demo.png)

