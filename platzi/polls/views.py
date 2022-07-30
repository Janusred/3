from ast import Try
from operator import ge
from django.urls import reverse
from django.shortcuts import  render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from pytz import timezone

from .models import Question, Choices

#def index(request):
 #   lastest_question_list = Question.objects.all()
  #  return render(request, "polls/index.html", {
   #     "lastest_question_list": lastest_question_list
    #})

#def detail(request, question_id):
 #   question = get_object_or_404(Question, pk=question_id)
  #  return render(request, "polls/detail.html",{
   #     "question":question
    #})

#def results(request, question_id):
 #   question = get_object_or_404(Question, pk=question_id)
  #  return render(request, "polls/results.html", {
   #     "question":question
    # })

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "lastest_question_list"

    def get_queryset(self):
        """Return ths last five questions"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name= "polls/detail.html"

class ResultView(generic.DetailView):
    model= Question
    template_name= "polls/result.html"



def vote(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        select_choices = question.choices_set.get(pk=request.POST["choices"])
    except (KeyError, Choices.DoesNotExist):
        return render(request,"polls/detail.html",{
            "question":question,
            "error_message": "No elegiste una respuesta"
        }) 
    else:
        select_choices.votes + 1
        select_choices.save()
        return HttpResponseRedirect(reverse("polls:results",args=(question.id)))
