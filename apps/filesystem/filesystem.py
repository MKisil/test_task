from .exceptions import FileOrDirectoryExistsError, FileOrDirectoryNotFoundError, InvalidPathError
from .utils import current_time


class Node:  # for file or directory
    def __init__(self):
        self.is_file = False
        self.children = {}
        self.content = ""

        time_creation = current_time()
        self.metadata = {
            "created": time_creation,
            "modified": time_creation,
            "size": 0
        }


class SimpleFileSystem:
    def __init__(self):
        self.__root = Node()

    def create_dir(self, path):
        curr = self.__create_node(path)
        curr.is_file = False

    def list_dir(self, path, sort_by=None):
        curr = self.__get_node(path)

        if curr.is_file:
            raise InvalidPathError("Path is a file.")

        entries = []

        for name, node in curr.children.items():
            entries.append({
                "name": name,
                "metadata": node.metadata,
                "is_file": node.is_file,
            })

        if sort_by == "size":
            entries.sort(key=lambda x: x["metadata"]["size"])
        elif sort_by == "modified":
            entries.sort(key=lambda x: x["metadata"]["modified"])

        return entries

    def create_file(self, filepath, content):
        curr = self.__create_node(filepath)
        curr.is_file = True
        curr.content = content
        curr.metadata["size"] = len(content)

        parent_path = self._get_parent_path(filepath)
        self._update_dirs_metadata(parent_path, len(content), curr.metadata["modified"])

    def read_file(self, filepath):
        curr = self.__get_node(filepath)
        if not curr.is_file:
            raise FileOrDirectoryNotFoundError(f"File not found")
        return curr.content

    def update_file(self, filepath, content):
        curr = self.__get_node(filepath)
        if not curr.is_file:
            raise FileOrDirectoryNotFoundError(f"File not found")
        curr.content = content
        size_change = len(content) - curr.metadata["size"]
        curr.metadata["modified"] = current_time()
        curr.metadata["size"] = len(content)
        parent_path = self._get_parent_path(filepath)
        self._update_dirs_metadata(parent_path, size_change, curr.metadata["modified"])

    def delete_dir_or_file(self, filepath):
        curr = self.__get_node(filepath)
        curr_size = curr.metadata["size"]
        self.__delete_node(filepath)
        parent_path = self._get_parent_path(filepath)
        self._update_dirs_metadata(parent_path, -curr_size, current_time())

    def _get_parent_path(self, path):
        return '/'.join(path.split('/')[:-1])

    def _update_dirs_metadata(self, path, size_add, modified):
        curr = self.__get_node(path)

        curr.metadata["modified"] = modified
        curr.metadata["size"] += size_add

        parent_path = self._get_parent_path(path)
        if parent_path:
            self._update_dirs_metadata(parent_path, size_add, modified)
        else:
            self.__root.metadata["modified"] = current_time()
            self.__root.metadata["size"] += size_add

    def __get_node(self, path):
        curr = self.__root
        path_split = self.__split(path)
        for i in path_split:
            curr = curr.children.get(i)
            if curr is None:
                raise FileOrDirectoryNotFoundError(f"File or directory not found.")
        return curr

    def __create_node(self, path):
        path = self.__normalize_path(path)
        if path in {'/', ''}:
            raise InvalidPathError("Cannot create a file or directory at root level.")

        curr = self.__root
        path_split = self.__split(path)
        for i in path_split:
            if curr.is_file:
                raise InvalidPathError("Cannot create a directory under a file.")
            if i in curr.children and i == path_split[-1]:
                raise FileOrDirectoryExistsError(f"File or directory already exists.")
            if i not in curr.children:
                curr.children[i] = Node()
            curr = curr.children[i]
        return curr

    def __delete_node(self, path):
        path_split = self.__split(path)
        if not path_split:
            raise InvalidPathError("Cannot delete root directory.")

        parent_path = '/' + '/'.join(path_split[:-1]) if len(path_split) > 1 else '/'
        parent_node = self.__get_node(parent_path)

        if path_split[-1] not in parent_node.children:
            raise FileOrDirectoryNotFoundError(f"File or directory not found.")

        del parent_node.children[path_split[-1]]

    def __split(self, path):
        if path == '/':
            return []
        return path.split('/')[1:]

    def __normalize_path(self, path):
        if not path.startswith('/'):
            raise InvalidPathError("Path must start with '/'.")
        return path.rstrip('/').replace('///', '//').replace('//', '/')


fs = SimpleFileSystem()