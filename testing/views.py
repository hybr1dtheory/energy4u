from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Question, Category, Testing, TestingQuestion
from random import randint
from datetime import datetime


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
        questions = Question.objects.all()[:10]
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
            ref = question.ref_name
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
    qid = randint(1, 60)
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
        ref_name = question.ref_name
        ref_url = question.ref_url
        correct = [v.id for v in variants if v.is_right]
        choice = int(request.session["one_choice"])  # get selected variant from user request
        if choice in correct:
            mess = "Правильна відповідь!"
        else:
            mess = "Нажаль відповідь неправильна. Скористайтеся посиланням на нормативний акт."
        del request.session["one_choice"]  # clean choice from session
        return render(request, "result.html",
                      {"choice": choice, "question": text,
                       "variants": variants, "message": mess,
                       "ref_name": ref_name, "ref_url": ref_url})
    else:
        return HttpResponseForbidden("Ви не відправили відповідь на це питання")


def exam_categories(request):
    """View to show the list of categories and choose the category for exam"""
    categories = Category.objects.all()
    return render(request, "exam_categories.html", {"categories": categories})


@login_required
def exam(request, category_id: int):
    """View gets the category id from url and generates a set of questions
    for specified category. View also process the data if request is post."""
    if request.method == "POST":
        answers = {}
        for i in range(1, 11):
            choice = request.POST.get(f"{i}", False)  # get every user choice from form by name
            if choice:
                qid, vid = choice.split(":")
                answers[qid] = vid
        request.session["exam_answers"] = answers  # writing answers to user session data
        request.session["exam_category"] = category_id
        request.session["exam_end"] = str(datetime.now())
        return HttpResponseRedirect("/exam/result")
    else:
        category = get_object_or_404(Category, pk=category_id)
        questions = Question.objects.filter(category_id__lte=category.id)[:10]
        request.session["exam_start"] = str(datetime.now())
        return render(request, 'exam.html',
                      {'questions_list': questions, 'selected': []})


@login_required
def exam_result(request):
    """View for getting results of the exam from user session
        and to send results to results page"""
    answers = request.session.get("exam_answers", False)  # get selected variants for all questions
    if answers:
        # creating data needed to save the result of the exam
        questions_data = []
        category_id = request.session.get("exam_category")
        exam_start = request.session.get("exam_start")
        exam_end = request.session.get("exam_end")
        exam_duration = datetime.fromisoformat(exam_end) - datetime.fromisoformat(exam_start)
        category = Category.objects.get(id=int(category_id))
        score = 0
        test = Testing(user=request.user, category=category, test_duration=exam_duration)
        test.save()
        for qid, vid in answers.items():
            question = Question.objects.get(id=int(qid))
            variants = question.variant_set.all()
            choice = variants.get(id=int(vid))
            user_answer = TestingQuestion(testing=test, question=question, variant=choice)
            user_answer.save()
            text = question.q_text
            ref = question.ref_name
            correct = variants.get(is_right=True).id
            if correct == choice.id:
                mess = "Правильна відповідь!"
                score += 1
            else:
                mess = "Нажаль відповідь неправильна. Скористайтеся посиланням на нормативний акт."
            q_data = {"choice": choice.id, "question": text,
                      "variants": variants, "message": mess, "reference": ref}
            questions_data.append(q_data)
        score *= 10
        test.result = score
        test.save()  # updating testing instance to save test result to the DB
        user_profile = request.user.profile
        avg_res, tests_count = user_profile.avg_result, user_profile.testing_count
        new_avg = (avg_res * tests_count + score) / (tests_count + 1)
        user_profile.avg_result = round(new_avg, 1)
        user_profile.testing_count = tests_count + 1
        user_profile.save()  # updating users average result and tests count
        return render(request, "exam_result.html",
                      {"questions_data": questions_data, "score": score})
    else:
        return HttpResponseForbidden("Ви не відправили відповідь на цей тест.")
