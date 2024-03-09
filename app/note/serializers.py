# serializers.py
from rest_framework import serializers

from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField())  # Specify ListField of CharField for
    # tags

    class Meta:
        model = Note
        fields = ['id', 'title', 'body',
                  'tags']  # Include id, title, body, and tags field in
        # serializer
