from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def owner(request):
    return HttpResponse("Hello, world. 11808b3e is the polls index.")

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    correct_answer = str(Choice.objects.get(choice_text="42"))
    context = {"question": question, "correct_answer": correct_answer}
    return render(request, "polls/detail.html", context)

def results(request, question_id):
    return HttpResponse(f"You're looking at the results of question {question_id}")

def vote(request, question_id):
    return HttpResponse(f"You're voting on question {question_id}.")
