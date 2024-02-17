from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from .models import Question
from random import randint


def index(request):
    """view function for main page of testing app"""
    num_questions = Question.objects.all().count()
    data = {"num_questions": num_questions}
    return render(request, "index.html", context=data)


def questions_list(request):
    """View for generating a set of random 10 questions
    and to process the data if request is post."""
    if request.method == "POST":
        answers = {}
        for i in range(1, 11):
            for j in range(1, 10):
                choice = request.POST.get(f"{i}{j}", False)
                if choice:
                    qid, vid = choice.split(":")
                    choice_list = answers.get(qid, [])
                    choice_list.append(vid)
                    answers[qid] = choice_list
        request.session["answers"] = answers
        return HttpResponseRedirect("test_result")
    else:
        q_num = randint(1, 90)
        questions = Question.objects.all()[q_num: q_num + 10]
        return render(request, 'questions.html', {'questions_list': questions})


def test_result(request):
    """View for getting results of the test from user session
    and to send results to results page"""
    answers = request.session.get("answers", False)  # get selected variants for all questions
    if answers:
        # creating data needed to view the result of the test
        questions_data = []
        for qid in answers:
            question = get_object_or_404(Question, pk=int(qid))
            choices = [int(c) for c in answers[qid]]
            variants = question.variant_set.all()
            text = question.q_text
            ref = question.reference
            correct = [v.id for v in variants if v.is_right]
            if correct == choices:
                mess = "Правильна відповідь!"
            else:
                mess = "Нажаль відповідь неправильна або неточна. Скористайтеся посиланням на нормативний акт."
            q_data = {"choices": choices, "question": text,
                      "variants": variants, "message": mess, "reference": ref}
            questions_data.append(q_data)

        return render(request, "test_result.html", {"questions_data": questions_data})
    else:
        return HttpResponseForbidden("Ви не відправили відповідь на цей тест.")


def one_quest(request):
    """Redirecting to random question"""
    qid = randint(1, 85)
    return HttpResponseRedirect(f"{qid}")


def one_quest_id(request, question_id):
    """This view get the question id from url and send question data
    if request method is not POST, else the view get choices
    to send results to the 'result' view."""
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        variants = [var.id for var in question.variant_set.all()]
        selected_variants = []
        for v in variants:
            choice = request.POST.get(f"variant{v}", False)
            if choice:
                selected_variants.append(choice)
        if selected_variants:
            request.session["choices"] = selected_variants

            return HttpResponseRedirect("result")
        else:
            return render(request, 'one_quest_id.html',
                          {'question': question, "error_message": "Оберіть варіант"})
    else:
        return render(request, 'one_quest_id.html', {'question': question})


def result(request, question_id):
    """This view process choices to show the result"""
    if request.session.get("choices", False):
        question = get_object_or_404(Question, pk=question_id)
        variants = question.variant_set.all()
        text = question.q_text
        ref = question.reference
        correct = [v.id for v in variants if v.is_right]
        choices = [int(c) for c in request.session["choices"]]  # get selected variants from user request
        if correct == choices:
            mess = "Правильна відповідь!"
        else:
            mess = "Нажаль відповідь неправильна або неточна. Скористайтеся посиланням на нормативний акт."
        del request.session["choices"]  # clean choices from session
        return render(request, "result.html",
                      {"choices": choices, "question": text,
                       "variants": variants, "message": mess, "reference": ref})
    else:
        return HttpResponseForbidden("Ви не відправили відповідь на це питання")
