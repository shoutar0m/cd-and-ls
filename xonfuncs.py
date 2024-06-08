# -*- coding: utf-8 -*-
import os
import sys


class CdAndLs:
    """ Change Directory And List All Components.

    This class has got attributes and methods to change directory and list components.

    Attributes:
        __home_dir_path (str): Path string to the home directory.
        __zero_space_japanese_characters (list[str]): Zero space Japanese characters.
        __total_name_length (int): Total name length. This should be longer than 12.
        __dirs_list_string_header (str): Header string of the directory names list string.
        __files_list_string_header (str): Header string of the file names list string.

    """

    def __init__(self, home_dir_path: str):
        self.__home_dir_path: str = home_dir_path
        self.__zero_space_japanese_characters: list[str] = ['゙', '゚']
        self.__total_name_length: int = 37
        self.__dirs_list_string_header: str = '------- directories -------'.center(int(self.__total_name_length * 1.35))
        self.__files_list_string_header: str = '------- files -------'.center(int(self.__total_name_length * 1.35))

    def change_directory(self, dest_path: str) -> str:
        """ Change directory and return its path string.

        Arg:
            dest_path (str): Destination directory path string.

        Return:
            This returns destination directory path string after moved.
        
        """

        os.chdir(dest_path)
        return os.getcwd()

    def get_all_components(self, path: str) -> tuple[list[str], list[str]]:
        """ Get and return all directory names and file names in the destination directory.
        
        Args:
            path (str): Path string. This method gets components in the directory of this 'path'.

        Returns:
            dir_names (list[str]): Directory names in the directory of the 'path'.
            file_names (list[str]): File names in the directory of the 'path'.

        """

        dir_names: list[str] = sorted([
            dir_name for dir_name in os.listdir(path)
            if os.path.isdir(os.path.join(path, dir_name))
        ], key=str.lower)

        file_names: list[str] = sorted([
            file_name for file_name in os.listdir(path)
            if os.path.isfile(os.path.join(path, file_name))
        ], key=str.lower)

        return dir_names, file_names

    def add_white_spaces(self, name: str, total_length: int, is_dir_name: bool = True) -> str:
        """ Add white spaces up to specified length.

        This adds white spaces to the string got as 'name' argument up to specified length.
        Then, this counts each character length as a 2 if it's not ascii character.

        Args:
            name (str): File name or Directory name.
            total_length (int): The number of max length of the return string. This should be longer than 12.
            is_dir_name (bool): The name is of directory or not.

        Returns:
            return_string (str): String with white spaces up to specified length.

        """

        current_length: int = 0
        return_string: str = ''

        for i in range(len(name)):
            return_string = return_string + name[i]

            # Count the number of the character length up to current index.
            # If the character of current index is ascii character, ...
            if name[i].isascii():
                current_length = current_length + 1  # Plus one.
            
            # If the character of current index is any zero space Japanese character, ...
            elif name[i] in self.__zero_space_japanese_characters:
                current_length = current_length + 0  # Plus zero.
            
            # If other cases, ...
            else:
                current_length = current_length + 2  # Plus two.

            # If the current length is over the specified, exits this loop and returns the current string.
            if current_length >= (total_length - (len('... /') - 2)):
                if name[i + 1] in self.__zero_space_japanese_characters:
                    return_string = return_string + name[i + 1]

                if is_dir_name:
                    return return_string + '... /' + (' ' * (total_length - (current_length + len('... /'))))
                    
                else:
                    return return_string + '... ' + (' ' * (total_length - (current_length + len('... '))))
            
        # If this loop finished without leaving, ...
        else:
            if is_dir_name:
                return return_string + '/' + (' ' * (total_length - 1 - current_length))
            
            else:
                return return_string + (' ' * (total_length - current_length))

    def create_stdout_string(self, dir_names: list[str], file_names: list[str]) -> str:
        """ Create and return stdout string.
        
        Args:
            dir_names (str): Directory names to create stdout string.
            file_names (str): File names to create stdout string.

        Return:
            This returns stdout string to display all components in the destination directory.

        """

        # Create a directory names list string body.

        dirs_list_string_body: str = ''
        for i in range(0, len(dir_names) - 1, 2):
            dirs_list_string_body = dirs_list_string_body + \
                self.add_white_spaces(name=dir_names[i], total_length=self.__total_name_length, is_dir_name=True) + \
                self.add_white_spaces(name=dir_names[i + 1], total_length=self.__total_name_length, is_dir_name=True) + '\n'

        if dir_names and (len(dir_names) % 2):
            dirs_list_string_body = dirs_list_string_body + \
                self.add_white_spaces(name=dir_names[-1], total_length=self.__total_name_length, is_dir_name=True)
            
        if not dirs_list_string_body:
            dirs_list_string_body = '↪︎ No Directories'
            
        # Create a file names list string body.
        files_list_string_body: str = ''
        for i in range(0, len(file_names) - 1, 2):
            files_list_string_body = files_list_string_body + \
                self.add_white_spaces(name=file_names[i], total_length=self.__total_name_length, is_dir_name=False) + \
                self.add_white_spaces(name=file_names[i + 1], total_length=self.__total_name_length, is_dir_name=False) + '\n'

        if file_names and (len(file_names) % 2):
            files_list_string_body = files_list_string_body + \
                self.add_white_spaces(name=file_names[-1], total_length=self.__total_name_length, is_dir_name=False)
        
        if not files_list_string_body:
            files_list_string_body = '↪︎ No files'

        return f'\n{self.__dirs_list_string_header}\n{dirs_list_string_body}\n\n' + \
            f'{self.__files_list_string_header}\n{files_list_string_body}'
    
    def cd_and_ls(self, stdins: list[str] = []) -> None:
        """ Main method of this class.

        Arg:
            stdins (list[str]): Standard input list.

        """

        try:
            # Get destination directory path from stdin.
            path: str = self.__home_dir_path
            if stdins[:1]:
                path = str(stdins[:1][0])
            
            # Display directory names nad file names in the destination directory.
            current_path: str = self.change_directory(dest_path=path)
            dir_and_file_names: tuple[list[str], list[str]] = self.get_all_components(path=current_path)
            print(self.create_stdout_string(*dir_and_file_names))
        
        except FileNotFoundError:
            print(f'\nNo such directory: "{path}"')
        
        except Exception as e:
            print(e)


if __name__ == '__main__':

    # Change Directory And List All Components.
    CdAndLs('path/to/home').cd_and_ls()
