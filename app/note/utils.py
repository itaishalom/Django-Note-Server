from rest_framework.exceptions import PermissionDenied
from django.db.models import Q

from .models import Note
from .serializers import NoteSerializer


def validate_user(note, user):
    if note.user != user:
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


def calculate_word_count(content):
    words = content.split()
    return len(words)
