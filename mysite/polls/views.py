from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from django.db.models import F
from .models import Question, Choice


# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "polls/index.html", context)

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list" # overrides ListView auto-generated 
    #                                              context var ('question_list')

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]

def owner(request):
    return HttpResponse("Hello, world. 11808b3e is the polls index.")

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id) - NOTE: in DetailView,
#           Django is able to determine an appropriate name for this context variable
#     correct_answer = Choice.objects.get(choice_text="42")
#     context = {"question": question, "correct_answer": correct_answer}
#     return render(request, "polls/detail.html", context)

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # AVOID RACE CONDITIONS WITH F() - error 'Choice' object has no attribute 'update':
        # selected_choice.update(votes=F("votes") + 1)
        # https://docs.djangoproject.com/en/4.2/ref/models/expressions/#avoiding-race-conditions-using-f

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    # NOTE:
    # reverse() function helps avoid having to hardcode a URL in the view function. 
    # It is given the name of the view that we want to pass control to and the 
    # variable portion of the URL pattern that points to that view.
    # (returns a string like "/polls/3/results/", 3 = question.id)