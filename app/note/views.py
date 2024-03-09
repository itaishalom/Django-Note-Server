# notes/views.py
from rest_framework import status, authentication, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from .models import Note
from .serializers import NoteSerializer


def _validate_user(note, request):
    if note.user != request.user:
        raise PermissionDenied(
            "You do not have permission to update this note.")


def get_notes(self, filter_conditions, page_size, request, paginator):
    notes = Note.objects.filter(filter_conditions).order_by('-id')
    if page_size:
        paginator.page_size = page_size
    paginated_notes = paginator.paginate_queryset(notes, request, view=self)
    serializer = NoteSerializer(paginated_notes, many=True)
    return paginator.get_paginated_response(serializer.data)


def get_params(request):
    page_size = request.query_params.get('page_size')
    tag = request.query_params.get('tag', None)
    query = request.query_params.get('query', None)
    return page_size, query, tag


def extract_params(request):
    title = request.data.get('title')
    body = request.data.get('body')
    tags = request.data.get('tags', [])
    note_data = {'title': title, 'body': body, 'tags': tags}
    return note_data


def generate_filter(query, tag, mandatory_filter):
    filter_conditions = mandatory_filter
    if tag:
        filter_conditions &= Q(tags__contains=tag)
    if query:
        filter_conditions &= Q(body__icontains=query)
    return filter_conditions


class UserNotes(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def get(self, request):

        page_size, query, tag = get_params(request)

        filter_conditions = generate_filter(query, tag, Q(user=request.user))
        return get_notes(self, filter_conditions, page_size, request,
                         self.pagination_class())

    def post(self, request):
        note_data = extract_params(request)
        serializer = NoteSerializer(data=note_data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, note_id):
        try:
            note = Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        _validate_user(note, request)

        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, note_id):
        try:
            note = Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        _validate_user(note, request)
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserNotesPublic(APIView):
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def get(self, request):
        page_size, query, tag = get_params(request)

        filter_conditions = generate_filter(query, tag,
                                            Q(privacy=Note.PRIVACY_CHOICES[0][
                                                0]))
        return get_notes(self, filter_conditions, page_size, request,
                         self.pagination_class())
