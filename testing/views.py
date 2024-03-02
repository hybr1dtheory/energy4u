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
            choice = request.POST.get(f"{i}", False)  # get every user choice from form by name
            if choice:
                qid, vid = choice.split(":")
                answers[qid] = vid
        if len(answers) < 10:
            mess = "Необхідно обрати варіант в кожному питанні!"
            selected = []
            questions = []
            for q, v in answers.items():
                selected.append(int(v))
                question = Question.objects.get(id=int(q))
                questions.append(question)
            return render(request, 'questions.html',
                          {'questions_list': questions, 'selected': selected, 'error_message': mess})
        else:
            request.session["answers"] = answers  # writing answers to user session data
            return HttpResponseRedirect("test_result")
    else:
        q_ids = set()
        while len(q_ids) < 10:  # generating 10 random id for questions set
            q_ids.add(randint(1, 40))
        questions = Question.objects.filter(id__in=q_ids)
        return render(request, 'questions.html',
                      {'questions_list': questions, 'selected': []})


def test_result(request):
    """View for getting results of the test from user session
    and to send results to results page"""
    answers = request.session.get("answers", False)  # get selected variants for all questions
    if answers:
        # creating data needed to show the result of the test
        questions_data = []
        score = 0
        for qid, vid in answers.items():
            question = Question.objects.get(id=int(qid))
            choice = int(vid)
            variants = question.variant_set.all()
            text = question.q_text
            ref = question.reference
            correct = variants.get(is_right=True).id
            if correct == choice:
                mess = "Правильна відповідь!"
                score += 1
            else:
                mess = "Нажаль відповідь неправильна. Скористайтеся посиланням на нормативний акт."
            q_data = {"choice": choice, "question": text,
                      "variants": variants, "message": mess, "reference": ref}
            questions_data.append(q_data)
        score *= 10
        return render(request, "test_result.html",
                      {"questions_data": questions_data, "score": score})
    else:
        return HttpResponseForbidden("Ви не відправили відповідь на цей тест.")


def one_quest(request):
    """Redirecting to random question"""
    qid = randint(1, 40)
    return HttpResponseRedirect(f"{qid}")


def one_quest_id(request, question_id):
    """This view get the question id from url and send question data
    if request method is not POST, else the view get choices
    to send results to the 'result' view."""
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        selected_variant = request.POST.get(f"{question_id}", False)
        if selected_variant:
            request.session["one_choice"] = selected_variant
            return HttpResponseRedirect("result")
        else:
            return render(request, 'one_quest_id.html',
                          {'question': question, "error_message": "Оберіть варіант"})
    else:
        return render(request, 'one_quest_id.html', {'question': question})


def result(request, question_id):
    """This view process choices to show the result"""
    if request.session.get("one_choice", False):
        question = get_object_or_404(Question, pk=question_id)
        variants = question.variant_set.all()
        text = question.q_text
        ref = question.reference
        correct = [v.id for v in variants if v.is_right]
        choice = int(request.session["one_choice"])  # get selected variant from user request
        if choice in correct:
            mess = "Правильна відповідь!"
        else:
            mess = "Нажаль відповідь неправильна. Скористайтеся посиланням на нормативний акт."
        del request.session["one_choice"]  # clean choice from session
        return render(request, "result.html",
                      {"choice": choice, "question": text,
                       "variants": variants, "message": mess, "reference": ref})
    else:
        return HttpResponseForbidden("Ви не відправили відповідь на це питання")
