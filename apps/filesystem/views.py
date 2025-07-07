from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .exceptions import FileOrDirectoryNotFoundError, FileOrDirectoryExistsError, InvalidPathError
from .filesystem import fs

class FileView(APIView):
    def get(self, request, path):
        try:
            return Response(fs.read_file(path))
        except FileOrDirectoryNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        path = request.data.get("path")
        content = request.data.get("content", "")
        try:
            fs.create_file(path, content)
            return Response({"message": "File created."}, status=status.HTTP_201_CREATED)
        except (FileOrDirectoryExistsError, InvalidPathError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, path):
        content = request.data.get("content", "")
        try:
            fs.update_file(path, content)
            return Response({"message": "File updated."})
        except FileOrDirectoryNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, path):
        try:
            fs.delete_dir_or_file(path)
            return Response({"message": "File deleted."})
        except FileOrDirectoryNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class DirectoryView(APIView):
    def get(self, request, path):
        sort_by = request.query_params.get("sort_by")
        try:
            return Response(fs.list_dir(path, sort_by=sort_by))
        except FileOrDirectoryNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        path = request.data.get("path", "")
        try:
            fs.create_dir(path)
            return Response({"message": "Directory created."}, status=status.HTTP_201_CREATED)
        except (FileOrDirectoryExistsError, InvalidPathError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, path):
        try:
            fs.delete_dir_or_file(path)
            return Response({"message": "Directory deleted."})
        except FileOrDirectoryNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
