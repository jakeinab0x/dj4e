import csv # https://docs.python.org/3/library/csv.html

import datetime
from django.utils import timezone

from polls.models import Question, Choice

def run():
    print("=== Polls Loader")

    Choice.objects.all().delete()
    Question.objects.all().delete()
    print("=== Objects deleted")

    fhand = open('scripts/dj4e_batch.csv')
    reader = csv.reader(fhand)
    next(reader) # Advance past the header

    for row in reader:
        print(row)
        question_text = row[0]
        choices = row[1:]
        q = Question(question_text=question_text, pub_date=timezone.now())
        q.save()

        for choice in choices:
            q.choice_set.create(choice_text=choice, votes=0)

    print("=== Load Complete")