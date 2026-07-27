from django.urls import path
from . import views
from .views import voice_callback, voice_events

app_name = 'voice'

urlpatterns = [
    path('callback/', voice_callback, name='voice-callback'),
    path('events/', voice_events, name='voice-events'),
    path('transcribe', views.transcribe_audio, name='transcribe'),
    path('process-command', views.process_voice_command, name='process_command'),
    path('context', views.get_voice_context, name='get_context'),
]