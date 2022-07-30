from audioop import reverse
import datetime
from urllib import response 

from django.test import TestCase
from django.utils import timezone

from .models import Question
def create_questin(question_tex, days):
    """
    Create a question wit the give "question_text", and published the
    given number offset
    """
    time=timezone.now + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    def test_published_recently_with_future_question(self):
        """was_published_recently returns flse for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(questions_text="Quien es le mejor alumno",pub_date=time)
        self.assertIs(future_question.was_published_recently(),False)
class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """if no question exist, an appropiate message is disployed"""
        response = self.client.get(reversed("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])
    
    def test_future_question(self):
        """Question"""
        create_question("Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are Avaiable")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])


    def test_past_question(self):
        """Question"""
        question=create_question("Pass question", days=10)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are Avaiable")
        self.assertQuerysetEqual(response.context["latest_question_list"],[question])


    def test_future_questions(self):
        """The question"""
        past_question= create_question(question_text="Past question",days=30)
        future_question = create_question(question_tex="question_text",days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question-list"],
            [past_question]
        )

    def test_past_question(self):
        """The question"""
        past_question1 = create_question(question_text="past question 1",days=-30)
        past_question2 = create_question(question_text="past question 2",days=-40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1,past_question2]
        )
