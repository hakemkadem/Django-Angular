from django.shortcuts import render

# Create your views here.

def Author_list(requst):
    return render(requst,'Authors/Authors.html');
