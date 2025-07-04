import time

from .exceptions import FileExistsError, FileNotFoundError

"""
    A simple in-memory file system implementation with basic file operations.
    Features:
    - Create, read, update, delete files
    - List files with optional sorting
    - Search files by name or content
    - Get file metadata
    - List files in a directory
    
    Search by filename is O(1) due to the use of a dictionary for filename indexing, case sensitive.
    Search by content is O(n) where n is the number of files, as it checks each file content. Not case sensitive. I thought about each word indexing, but it would not support phrases.
"""


class SimpleFileSystem:
    def __init__(self):
        self.files = {}  # filepath -> content
        self.metadata = {}  # filepath -> metadata (created, modified, size)
        self.filename_index = {}  # filename -> set of filepaths

    def _update_index_on_create(self, path):
        filename = path.split('/')[-1]
        self.filename_index.setdefault(filename, set()).add(path)

    def _update_index_on_delete(self, path):
        filename = path.split('/')[-1]
        if filename in self.filename_index:
            self.filename_index[filename].discard(path)
            if not self.filename_index[filename]:
                del self.filename_index[filename]

    def create_file(self, name, content):
        if name in self.files:
            raise FileExistsError(f"File '{name}' already exists.")
        self.files[name] = content
        now = time.time()
        self.metadata[name] = {
            "created": now,
            "modified": now,
            "size": len(content.encode('utf-8'))
        }
        self._update_index_on_create(name)

    def read_file(self, name):
        if name not in self.files:
            raise FileNotFoundError(f"File '{name}' not found.")
        return self.files[name]

    def update_file(self, name: str, content: str) -> None:
        if name not in self.files:
            raise FileNotFoundError(f"File '{name}' not found.")
        self.files[name] = content
        self.metadata[name]["modified"] = time.time()
        self.metadata[name]["size"] = len(content.encode('utf-8'))

    def delete_file(self, name: str) -> None:
        if name not in self.files:
            raise FileNotFoundError(f"File '{name}' not found.")
        self._update_index_on_delete(name)
        del self.files[name]
        del self.metadata[name]

    def list_files(self, sort_by=None) :
        files_list = list(self.files.keys())
        if sort_by == "name":
            files_list.sort()
        elif sort_by == "size":
            files_list.sort(key=lambda f: self.metadata[f]["size"])
        return files_list

    def search_by_filename(self, query):
        result = []
        query_lower = query.lower()
        for filename, paths in self.filename_index.items():
            if query_lower in filename.lower():
                result.extend(paths)
        return sorted(result)

    def search_by_content(self, query):
        query = query.lower().strip()
        result = []
        if not query:
            return result
        for name, content in self.files.items():
            if query in content.lower():
                result.append(name)
        return sorted(result)


    def get_metadata(self, name):
        if name not in self.metadata:
            raise FileNotFoundError(f"File '{name}' not found.")
        return self.metadata[name].copy() # prevent form external modification

    def list_dir(self, directory: str = ""):
        if directory and not directory.endswith('/'):
            directory += '/'
        files_in_dir = [f[len(directory):] for f in self.files if
                        f.startswith(directory) and '/' not in f[len(directory):]]
        return sorted(files_in_dir)


fs = SimpleFileSystem()