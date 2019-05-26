from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('groups', views.groupselect, name='groupselect'),
    path('generate', views.get_sentence, name='generate'),
    path('newword', views.new_word, name='newword'),
    path('deleteword', views.delete_word, name='deleteword'),
]
