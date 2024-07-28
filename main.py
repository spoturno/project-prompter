import os
import sys
import pyperclip

def read_files_in_folders(project_path, output_file_path, folders, ignore_extensions, copy_to_clipboard=False):
    content = ""
    with open(output_file_path, 'w') as output_file:
        for folder in folders:
            folder_path = os.path.join(project_path, folder)
            if not os.path.exists(folder_path):
                print(f"Folder '{folder}' does not exist in the project path.")
                continue
            
            for root, _, files in os.walk(folder_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    if any(file_name.lower().endswith(ext) for ext in ignore_extensions):
                        continue
                    try:
                        with open(file_path, 'r') as file:
                            relative_path = os.path.relpath(file_path, project_path)
                            file_content = file.read()
                            output_file.write(f"{relative_path}:\n```\n")
                            output_file.write(file_content)
                            output_file.write("\n```\n\n")
                            content += f"{relative_path}:\n```\n{file_content}\n```\n\n"
                    except Exception as e:
                        print(f"Error reading file '{file_path}': {e}")

    if copy_to_clipboard:
        pyperclip.copy(content)
        print("Content copied to clipboard.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py <project_path> <output_file_path> <folder1> <folder2> ... [--clipboard]")
        sys.exit(1)

    project_path = sys.argv[1]
    output_file_path = sys.argv[2]
    folders = []
    copy_to_clipboard = False

    for arg in sys.argv[3:]:
        if arg == "--clipboard":
            copy_to_clipboard = True
        else:
            folders.append(arg)

    ignore_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg']

    read_files_in_folders(project_path, output_file_path, folders, ignore_extensions, copy_to_clipboard)
