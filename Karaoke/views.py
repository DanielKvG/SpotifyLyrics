from django.shortcuts import render
from json import dumps
from .main import g 

# Create your views here.
def index(request):

    text = g.GetLyrics()
    length = g.GetLength()
    progress = g.GetProgress()


    lyrics = {
        "liedje" : text,
        "length" : length,
        "progress" : progress
    }
        
    return render(request, './karaoke/index.html', lyrics)


    