import os
from datetime import datetime
from rich.console import Console
from rich.table import Table

from .utils import *

console = Console()
CUR_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CUR_DIR)

class CliApp():
    """Command line interface for Integripy
    """
    
    def __init__(self) -> None:
        try:
            self._app_loop()
        except KeyboardInterrupt:
            self.quit()
            
         
    def _app_loop(self):
        """App main loop
        """
        while True:
            self.main_menu()
            
    
    "MENUS FUNCTIONS"
    def show_menu(self, title: str, choices: list[tuple] | None) -> None:
        """Show the given menu and choices

        Args:
            title (str): Menu title
            choices (list[tuple] | None): Menu choices
        """
        
        # Clear the console
        display.clear()
        
        # Display the app title
        display.app_title()
        
        # Display the menu title
        display.menu_title(title)
        
        # If choices given, list the choices in console
        if choices:
            for i, choice in enumerate(choices):
                    console.print(f"{i+1}. {choice[0]}")
                
    def quit_menu(self):
        """Quit the current menu
        """
        return
        
    def menu_func(self, choices: list[tuple[str, callable]], choice: int, *args):
        """Call the function specified in the list of choices

        Args:
            choices (list[tuple[str, callable]]): List of choices
            choice (int): Menu choice
            *args: Arguments for the function

        Returns:
            Any: returns of the called function
        """        
        return self._call_func(choices[choice-1][1], *args)
        
    def _call_func(self, func: callable, *args):
        """Call the given function with the given arguments

        Args:
            func (callable): Function to call
            *Args: Arguments for the function

        Returns:
            Any: returns of the called function
        """        
        return func(*args)
        
        
    "MAIN MENU"
    def main_menu(self) -> None:
        """Run the main menu
        """
        
        menu_choices = [
            ("File hash menu", self.filehash_menu),  
            ("File integrity menu", self.fileintegrity_menu),
            ("Credits", self.credits_menu),
            ("Quit", self.quit)   
        ]
        
        # Display main menu
        self.show_menu('MAIN MENU', menu_choices)
        
        # Handles the choices
        choice = prompt.ask_choice(menu_choices)
        self.menu_func(menu_choices, choice)
        
        
    "FILE HASH MENU"        
    def filehash_menu(self) -> None:
        """Run the filehash menu
        """
        
        menu_choices = [
            ("Get sha256", filehash.get_sha256),  
            ("Get MD5", filehash.get_md5),
            ("Get both", filehash.get_both),
            ("Get all", filehash.get_all),
            ("Main menu", self.quit_menu)
        ]
        
        # Func to create the hash table
        def create_hashtable() -> Table:
            table = Table(show_header=True, header_style="bold green", caption="File hash table", show_lines=True, title_style="magenta", title_justify="left")
            table.add_column("Algorithm")
            table.add_column("Hash", overflow="fold", style="dim")
            return table
        
        # Func to get the hashed file info
        def get_file_info(path: str) -> dict:
            name = os.path.basename(path)
            creation_date = datetime.fromtimestamp(os.path.getctime(path)).strftime("%d/%m/%Y")
            return {'name': name, 'creation_date': creation_date, 'size': os.path.getsize(path)}
        
        
        # Display the menu
        self.show_menu('FILE HASH MENU', menu_choices)
        
        # Menu loop
        while True:
            
            # Ask the user to choice a hash method
            choice = prompt.ask_choice(menu_choices)
            
            # If the user select back to main menu, left
            if menu_choices[choice-1][1] == self.quit_menu:
                return
        
            # Try to get the file path
            try: 
                path = prompt.ask_path()
            except:
                console.print("Invalid path", style="red")
                continue
                        
            try:
                # Creating the hash table
                table = create_hashtable()
               
                # Adding the file info to the table title 
                file_info = get_file_info(path)
                table.title = f" {file_info['name']} - {file_info['size']} bytes - {file_info['creation_date']}"
                
                # Fill the table with hashes
                match self.menu_func(menu_choices, choice, path):
                    
                    # Unique hash
                    case var if type(var) == tuple:
                        table.add_row(var[0], var[1])
                        
                    # Multiple hash
                    case var if type(var) == list:
                        for h in var:
                            table.add_row(h[0], h[1])
                    
                    # Other
                    case _:
                        return
                    
                # Display the table
                console.print(table, new_line_start=True, crop=False)
                
            except:
                console.print("An error occurred!", style="red")

                
    "FILE INTEGRITY MENU"
    def fileintegrity_menu(self) -> None:
        """Run the file integrity menu
        """
        
        menu_choices = [
            ("Check file integrity", self.check_integrity),
            ("List supported algorithms", self.list_algorithms),
            ("Main menu", self.quit_menu)
        ]
        
        # Display the menu
        self.show_menu('FILE INTEGRITY MENU', menu_choices)
        
        # Menu loop
        while True:
            
            # Ask the user to choose an option
            choice = prompt.ask_choice(menu_choices)
            
            # If the user select back to main menu, left
            if menu_choices[choice-1][1] == self.quit_menu:
                return
            
            # Try do execute the user choice
            try:
                self.menu_func(menu_choices, choice)
            except:
                console.print("An error occured!", style="red")
        
    def check_integrity(self) -> None:
        """Check the file integrity
        """        
        
        # Geting the file path
        try: 
            path = prompt.ask_path()
            expected_hash = prompt.ask_hash()
            
        except:
            console.print("Invalid path", style="red")
            return
            
        
        # Get all possible hash for the file (supported algo only)
        file_hash = filehash.get_all(path)
        
        # Chek if one of the hash is corresponding to the expected one
        for algo, hash in file_hash:
            if hash == expected_hash:
                console.print(f"Hash found with {algo}", style="green")
                return

        # If no hash correspond print a warning about file integrity
        console.print(f"Hash not found", style="bright_red")
        console.print(f"\n⚠️ File integrity could be compromised!", style="red")
        
    def list_algorithms(self) -> None:
        """List available algorithms
        """
        
        # Get the available algorithms
        algo_list = filehash.list_algorithms()
        
        # Display the list of algorithms
        console.print(f"\nSupported algorithms ({len(algo_list)})", end=" ")
        console.print(algo_list)  
        
        
    "CREDITS MENU"
    def credits_menu(self) -> None:
        """Displays information about author and licence
        """
        # Clear the console
        display.clear()
                
        # Game title
        display.app_title()
        
        # Project description
        display.section_title("DESCRIPTION")
        console.print("A tool for file integrity checking, dev in \"Cybersécurité\" course at EPSI Lille", highlight=False)
        console.print("Created in april 2024", style="dim italic", highlight=False)
        
        # Author infos
        display.section_title("AUTHOR INFOS")
        console.print("Name: Danaël LEGRAND")
        console.print("Email: danael.legrand@outlook.fr")
        console.print("Github: https://github.com/DCodeProg")
        
        # Colored DCodeProg
        console.print(r"""
[blue] ___  [/blue][bright_white] ___         _    [/bright_white][red] ___               [/red]
[blue]|   \ [/blue][bright_white]/ __|___  __| |___[/bright_white][red]| _ \_ _ ___  __ _ [/red]
[blue]| |) |[/blue][bright_white] (__/ _ \/ _` / -_)[/bright_white][red]  _/ '_/ _ \/ _` |[/red]
[blue]|___/ [/blue][bright_white]\___\___/\__,_\___[/bright_white][red]|_| |_| \___/\__, |[/red]
                                     [red]|___/  [/red]""", highlight=False)

        
        # Licence infos
        display.section_title("LICENCE")
        try:
            with open(os.path.join(ROOT_DIR, "LICENSE"), "r") as file:
                console.print(file.read(), highlight=False)
        except:
            console.print("Licence file not found!", style="red")
            console.print("[link=https://github.com/DCodeProg/Integripy/blob/main/LICENSE]See the licence on github[/link=https://github.com/DCodeProg/Integripy/blob/main/LICENSE]")
        
        # Back to main menu prompt
        prompt.back_to_main_menu()                
                
                
    "OTHER"
    def quit(self):
        """Exit the program
        """
        display.goodbye(False)
        quit()