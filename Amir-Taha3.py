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

        dest_folders = dest_path.split("/")
        dest_file_name = dest_folders.pop()
        dest_folder = self.root
        for name in dest_folders:
            if name in dest_folder.contents and isinstance(dest_folder.contents[name], Folder):
                dest_folder = dest_folder.contents[name]
            else:
                raise ValueError(f"Folder '{name}' not found.")

        src_file.rename(dest_file_name)
        dest_folder.add_file(src_file)

    def cp(self, src_path, dest_path):
        content = self.cat(src_path)
        self.create_file(dest_path, content)

    def create_file(self, path, content):
        folders = path.split("/")
        file_name = folders.pop()
        folder = self.root
        for name in folders:
            if name in folder.contents and isinstance(folder.contents[name], Folder):
                folder = folder.contents[name]
            else:
                raise ValueError(f"Folder '{name}' not found.")

        new_file = File(file_name, content)
        folder.add_file(new_file)

    def rm(self, path):
        folders = path.split("/")
        name = folders.pop()
        folder = self.root
        for name_part in folders:
            if name_part in folder.contents and isinstance(folder.contents[name_part], Folder):
                folder = folder.contents[name_part]
            else:
                raise ValueError(f"Folder '{name_part}' not found.")
        folder.remove(name)

    def save(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(self.root, f)

    def load(self, file_path):
        with open(file_path, 'rb') as f:
            self.root = pickle.load(f)
        self.current_folder = self.root

    def fragment(self, file_path):
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        with open(file_path, 'w') as f:
            for line in lines:
                f.write(f"{line}\n")


def main():
    fs = FileSystem()
    
    while True:
        command = input("Enter command: ").strip()
        
        if command.startswith("cd "):
            try:
                fs.cd(command[3:])
            except Exception as e:
                print(f"Error: {e}")
                
        elif command == "ls":
            try:
                contents = fs.ls()
                print("\n".join(contents))
            except Exception as e:
                print(f"Error: {e}")
                
        elif command.startswith("cat "):
            try:
                content = fs.cat(command[4:])
                print(content)
            except Exception as e:
                print(f"Error: {e}")
                
        elif command.startswith("mv "):
            try:
                paths = command[3:].split(" ")
                if len(paths) == 2:
                    fs.mv(paths[0], paths[1])
                else:
                    print("Invalid command format.")
            except Exception as e:
                print(f"Error: {e}")
                
        elif command.startswith("cp "):
            try:
                paths = command[3:].split(" ")
                if len(paths) == 2:
                    fs.cp(paths[0], paths[1])
                else:
                    print("Invalid command format.")
            except Exception as e:
                print(f"Error: {e}")
                
        elif command.startswith("rm "):
            try:
                fs.rm(command[3:])
            except Exception as e:
                print(f"Error: {e}")
                
        elif command.startswith("mkdir "):
            try:
                fs.mkdir(command[6:])
            except Exception as e:
                print(f"Error: {e}")
                
        elif command.startswith("save "):
            try:
                fs.save(command[5:])
            except Exception as e:
                print(f"Error: {e}")
                
        elif command.startswith("load "):
            try:
                fs.load(command[5:])
            except Exception as e:
                print(f"Error: {e}")
                
        elif command.startswith("fragment "):
            try:
                fs.fragment(command[9:])
            except Exception as e:
                print(f"Error: {e}")
                
        elif command == "exit":
            break
            
        else:
            print("Invalid command.")
            
if __name__ == "__main__":
    main()
