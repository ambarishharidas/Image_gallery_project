from unicodedata import category
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from pymongo import MongoClient
import gridfs
from django.http import JsonResponse
import os
def index(request):
    print(request.method)
    d = {'h1':1234}
    return render(request,'index.html',{})

def load(request):
    connection = MongoClient('mongodb://localhost:27017/')
    database = connection['gallery']
    """
    fs = gridfs.GridFS(database)
    data = fs.find({'filename':'file1'})
    latest = [x for x in data]
    #data = fs.get_last_version('file1').read()
    print(os.getcwd())
    
    f=open('gallery/static/file.jpg','wb')
    f.write(latest[0].read())
    f.close()
    """
    print(os.getcwd())
    category = request.GET['im']
    files_id = list(database.images.find({'category':category}))
    count = 1
    
    for x in os.listdir('gallery/static/images'):
        os.remove('gallery/static/images/'+x)
    print("REMOVED OLD IMAGES")
    fs = gridfs.GridFS(database)
    for file in files_id:
        data = [x for x in fs.find({'filename':file['_id']})]
        content = data[0].read()
        with open('gallery/static/images/'+category+str(count)+'.jpg','wb') as f:
            f.write(content)
        count+=1
    print("CREATED NEW IMAGES")
    data_urls = {}
    #print(os.listdir('gallery/static/images'))
    for c in os.listdir('gallery/static/images'):
        data_urls[c]='/static/images/'+c
    print(data_urls)
    return JsonResponse(data_urls,safe=False)

def displaybig(request):
    if request.method=='GET':
        print(request.GET)
        data = {'imagepath':'/static/images/'+request.GET['imagename']}
        return JsonResponse(data,safe=False)

