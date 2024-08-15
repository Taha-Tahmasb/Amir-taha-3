import pickle

class File:
    def __init__(self, name, content=""):
        self.name = name
        self.content = content

    def rename(self, new_name):
        self.name = new_name

    def edit_line(self, line_number, new_content):
        lines = self.content.split("\n")
        if 0 <= line_number < len(lines):
            lines[line_number] = new_content
            self.content = "\n".join(lines)
        else:
            raise ValueError("Line number out of range.")

    def delete_line(self, line_number):
        lines = self.content.split("\n")
        if 0 <= line_number < len(lines):
            lines.pop(line_number)
            self.content = "\n".join(lines)
        else:
            raise ValueError("Line number out of range.")
    
    def read_content(self):
        return self.content

class Folder:
    def __init__(self, name):
        self.name = name
        self.contents = {}

    def add_file(self, file):
        if file.name in self.contents:
            raise ValueError("File or Folder with this name already exists.")
        self.contents[file.name] = file

    def add_folder(self, folder):
        if folder.name in self.contents:
            raise ValueError("File or Folder with this name already exists.")
        self.contents[folder.name] = folder

    def remove(self, name):
        if name in self.contents:
            del self.contents[name]
        else:
            raise ValueError("File or Folder not found.")

    def list_contents(self):
        return list(self.contents.keys())

    def search(self, name=None, extension=None):
        results = []
        for item in self.contents.values():
            if isinstance(item, File):
                if name and item.name == name:
                    results.append(item)
                elif extension and item.name.endswith(extension):
                    results.append(item)
            elif isinstance(item, Folder):
                results.extend(item.search(name, extension))
        return results

class FileSystem:
    def __init__(self):
        self.root = Folder("root")
        self.current_folder = self.root

    def cd(self, path):
        folders = path.split("/")
        folder = self.root
        for name in folders:
            if name in folder.contents and isinstance(folder.contents[name], Folder):
                folder = folder.contents[name]
            else:
                raise ValueError(f"Folder '{name}' not found.")
        self.current_folder = folder

    def mkdir(self, name):
        new_folder = Folder(name)
        self.current_folder.add_folder(new_folder)

    def ls(self):
        return self.current_folder.list_contents()

    def cat(self, path):
        folders = path.split("/")
        file_name = folders.pop()
        folder = self.root
        for name in folders:
            if name in folder.contents and isinstance(folder.contents[name], Folder):
                folder = folder.contents[name]
            else:
                raise ValueError(f"Folder '{name}' not found.")
        
        if file_name in folder.contents and isinstance(folder.contents[file_name], File):
            return folder.contents[file_name].read_content()
        else:
            raise ValueError(f"File '{file_name}' not found.")

    def mv(self, src_path, dest_path):
        src_folders = src_path.split("/")
        src_file_name = src_folders.pop()
        src_folder = self.root
        for name in src_folders:
            if name in src_folder.contents and isinstance(src_folder.contents[name], Folder):
                src_folder = src_folder.contents[name]
            else:
                raise ValueError(f"Folder '{name}' not found.")

        if src_file_name in src_folder.contents and isinstance(src_folder.contents[src_file_name], File):
            src_file = src_folder.contents.pop(src_file_name)
        else:
            raise ValueError(f"File '{src_file_name}' not found.")