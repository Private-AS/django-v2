from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from .models import Question, Choice, Poll, PollSubmission
from django.template import loader
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.forms import modelformset_factory
from django.shortcuts import redirect
from .forms import PollForm, QuestionForm, ChoiceForm
# Create your views here.


def home(request):
    return render(request, 'polls/home.html', {})


def poll(request, id):
    try:
        poll_obj = Poll.objects.get(poll_id=id)
        question_list = Question.objects.filter(poll=poll_obj)
        template = loader.get_template('polls/poll.html')
        context = {
            'poll': poll_obj,
            'question_list': question_list,
        }
        return HttpResponse(template.render(context, request))
    except Poll.DoesNotExist:
        return HttpResponse("Poll not found.", status=404)


def save(request):
    if request.method == 'POST':
        poll_id = request.POST.get('poll_id')
        poll_obj = get_object_or_404(Poll, poll_id=poll_id)

        # Check if the user is authenticated
        if request.user.is_authenticated:
            # For logged-in users, check if they have already submitted this poll
            if PollSubmission.objects.filter(poll=poll_obj, user=request.user).exists():
                return HttpResponse("You have already submitted this poll.", status=400)
        else:
            # Check session for unauthenticated users
            submitted_polls = request.session.get('submitted_polls', [])
            if poll_id in submitted_polls:
                return HttpResponse("You have already submitted this poll.", status=400)

        # Process the poll submission
        for key, value in request.POST.items():
            if key not in ["csrfmiddlewaretoken", "poll_id"]:
                selected_choice = Choice.objects.get(id=value)
                selected_choice.votes += 1
                selected_choice.save()

        # Track submission
        if request.user.is_authenticated:
            PollSubmission.objects.create(poll=poll_obj, user=request.user)
        else:
            submitted_polls.append(poll_id)
            request.session['submitted_polls'] = submitted_polls

        return HttpResponse("Answers saved!")
    return HttpResponse("Invalid request method.", status=405)


@login_required
def answers(request, id):
    poll_obj = get_object_or_404(Poll, poll_id=id)
    if poll_obj.created_by != request.user:
        return HttpResponseForbidden("You are not authorized to view this page.")

    question_list = Question.objects.filter(poll=poll_obj)

    return render(request, 'polls/answers.html', {
        'poll': poll_obj,
        'question_list': question_list,
    })


@login_required
def your_polls(request):
    polls = Poll.objects.filter(created_by=request.user)
    poll_data = []

    for poll in polls:
        questions = []
        for question in poll.question_set.all():
            total_votes = question.choice_set.aggregate(Sum('votes'))['votes__sum'] or 0
            choices = []
            for choice in question.choice_set.all():
                percentage = (choice.votes / total_votes * 100) if total_votes > 0 else 0
                choices.append({
                    'choice': choice,
                    'percentage': percentage,
                    'percentage_display': f"{percentage:.2f}%",
                })
            questions.append({
                'question': question,
                'choices': choices,
                'total_votes': total_votes,
            })
        poll_data.append({
            'poll': poll,
            'questions': questions,
        })

    return render(request, 'polls/your_polls.html', {'poll_data': poll_data})


@login_required
def your_answers(request):
    submissions = PollSubmission.objects.filter(user=request.user)
    submitted_polls = []

    for submission in submissions:
        poll = submission.poll
        questions = Question.objects.filter(poll=poll)
        answers = []

        for question in questions:
            selected_choice = Choice.objects.filter(question=question, votes__gt=0).first()
            answers.append({
                'question': question,
                'selected_choice': selected_choice,
            })

        submitted_polls.append({
            'poll': poll,
            'answers': answers,
        })

    return render(request, 'polls/your_answers.html', {'submitted_polls': submitted_polls})


@login_required
def your_account(request):
    return render(request, 'polls/your_account.html', {'user': request.user})



@login_required
def create(request):
    QuestionFormSet = modelformset_factory(Question, form=QuestionForm, extra=1)
    ChoiceFormSet = modelformset_factory(Choice, form=ChoiceForm, extra=2)

    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        question_formset = QuestionFormSet(request.POST, queryset=Question.objects.none())
        choice_formset = ChoiceFormSet(request.POST, queryset=Choice.objects.none())

        if poll_form.is_valid() and question_formset.is_valid() and choice_formset.is_valid():
            poll = poll_form.save(commit=False)
            poll.created_by = request.user
            poll.save()

            for question_form in question_formset:
                if question_form.cleaned_data:
                    question = question_form.save(commit=False)
                    question.poll = poll
                    question.save()

                    for choice_form in choice_formset:
                        if choice_form.cleaned_data:
                            choice = choice_form.save(commit=False)
                            if choice.question_id is None:
                                choice.question = question
                            choice.save()

            return redirect('your_polls')

    else:
        poll_form = PollForm()
        question_formset = QuestionFormSet(queryset=Question.objects.none())
        choice_formset = ChoiceFormSet(queryset=Choice.objects.none())

    return render(request, 'polls/create.html', {
        'poll_form': poll_form,
        'question_formset': question_formset,
        'choice_formset': choice_formset,
    })

