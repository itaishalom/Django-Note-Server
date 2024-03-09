from django.urls import path

from . import views
from .views import UserNotes, UserNotesPublic

urlpatterns = [
    path('', UserNotes.as_view(), name='get'),
    path('public/', UserNotesPublic.as_view(), name='get'),
    path('', UserNotes.as_view(), name='post'),
    path('<int:note_id>', UserNotes.as_view(), name='delete'),
    path('<int:note_id>', UserNotes.as_view(), name='update'),
]
