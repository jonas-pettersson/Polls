from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('Hello!')


def detail(request, question_id):
    return HttpResponse(f'You are looking at question {question_id}')


def results(request, question_id):
    return HttpResponse(f'You are looking at the results of question {question_id}')


def vote(request, question_id):
    return HttpResponse(f'You are looking at the vote of question {question_id}')
