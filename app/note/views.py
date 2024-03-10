# notes/views.py
from rest_framework import status, authentication, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from .models import Note
from .serializers import NoteSerializer
from .utils import get_params, generate_filter, get_notes, extract_params, \
    validate_user


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

        validate_user(note, request.user)

        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, note_id):
        try:
            note = Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        validate_user(note, request.user)
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
