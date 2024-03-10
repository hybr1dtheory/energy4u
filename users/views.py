from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from testing.models import Testing, TestingQuestion


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт {username} був створений: можна увійти на сайт.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Ваш профіль оновлено.')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)


@login_required
def testing_history(request):
    user_id = request.user.id
    testings = Testing.objects.filter(user_id=user_id)
    return render(request, 'testing_history.html', {"testings": testings})


@login_required
def testing_details(request, testing_id: int):
    test_questions = TestingQuestion.objects.filter(testing_id=testing_id)
    choices = [tq.variant.id for tq in test_questions]
    test_result = Testing.objects.get(id=testing_id).result
    return render(request, 'testing_details.html',
                  {"test_questions": test_questions, "result": test_result, "choices": choices})
