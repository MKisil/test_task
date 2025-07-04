from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .exceptions import FileExistsError, FileNotFoundError
from .filesystem import fs

class FileListView(APIView):
    def get(self, request):
        sort_by = request.query_params.get("sort_by")
        return Response(fs.list_files(sort_by))

    def post(self, request):
        name = request.data.get("name")
        content = request.data.get("content", "")
        try:
            fs.create_file(name, content)
            return Response({"message": "File created."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FileDetailView(APIView):
    def get(self, request, name):
        try:
            return Response({"content": fs.read_file(name)})
        except FileNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, name):
        content = request.data.get("content", "")
        try:
            fs.update_file(name, content)
            return Response({"message": "File updated."})
        except FileNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, name):
        try:
            fs.delete_file(name)
            return Response({"message": "File deleted."})
        except FileNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class FilenameSearchView(APIView):
    def get(self, request):
        query = request.query_params.get("q", "")
        return Response(fs.search_by_filename(query))


class ContentSearchView(APIView):
    def get(self, request):
        query = request.query_params.get("q", "")
        return Response(fs.search_by_content(query))


class MetadataView(APIView):
    def get(self, request, name):
        try:
            return Response(fs.get_metadata(name))
        except FileNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class DirectoryView(APIView):
    def get(self, request):
        path = request.query_params.get("path", "")
        return Response(fs.list_dir(path))
