# Change Directory AND LiSt all components
![demo](./imgs/demo.png)
I created a function works as a command on xonsh shell.  

If you put this xonfuncs.py module in any directory and add some lines to the `.xonshrc`, your terminal app shows all components in the destination directory, as if you execute the `ls -a` (**LiSt All components**) UNIX/LINUX command together, every time you execute the `cd` (**Change Directory**) UNIX/LINUX command. 

(Currently, this function works correctly only in **English** or **Japanese**.)

## Requirements
- Python>=3.10.5
- xonsh>=0.13.3

## How to use
1.  Clone this repository by the following command.

	```
	git clone "https://github.com/shoutar0/cd-and-ls"
	```

2. Create `.xonshrc` if you have not.
3. Add some lines as the following to the `.xonshrc`.

	```.xonshrc
	import sys
	sys.path.append('path/to/myfunc.py')
	
	from xonfuncs import CdAndLs
	
	
	# Declare a function.
	def cd_and_ls(arg):
	    """ List all components after changing a directory. """
	    
	    try:
            if arg[:1]:
                path = str(arg[:1][0])
            else:
                path = 'path/to/home'

            func = CdAndLs()
            func.main(path)

        except FileNotFoundError:
            print(f'\nNo such directory: "{path}"')
	
	
	# Declare an alias.
	aliases['cd'] = cd_and_ls
	```

4. Launch your terminal app and try the `cd` command like the following. 

	```
	cd Development/Python/xonsh_func  # Example
	```
	
5. Your terminal must show like the following figure.
![demo](./imgs/demo.png)
