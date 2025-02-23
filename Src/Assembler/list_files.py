import os
import subprocess
import assembler

def list_files(folder):
    files = os.listdir(folder)
    files = [file for file in files if file.endswith(".asm")]
    return files

def display_file_content(file_path):
    with open(file_path, 'r') as file:
        print("\n--- File Content ---\n")
        print(file.read())
        print("\n--------------------\n")

def choose_file(files, folder):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Available assembly files:")
        for i, file in enumerate(files):
            print(f"[{i}] {file}")
        
        choice = input("Enter the index of the file you want to execute or 'exit' to quit: ").strip().lower()
        
        if choice == "exit":
            print("Exiting...")
            exit()
        
        try:
            index = int(choice)
            if 0 <= index < len(files):
                file_path = os.path.join(folder, files[index])
                display_file_content(file_path)
                confirm = input("Are you sure you want to execute this file? (y/n): ").strip().lower()
                if confirm == 'y':
                    return files[index]
            else:
                print("Invalid index. Try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number or 'exit'.")

if __name__ == "__main__":
    folder = "AssemblyCodes"
    files = list_files(folder)
    
    if not files:
        print("No assembly files found in the folder.")
    else:
        selected_file = choose_file(files, folder)
        file_path = os.path.join(folder, selected_file) 
        assembler.process_assembly(file_path, "out.txt")  

