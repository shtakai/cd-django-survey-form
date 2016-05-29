from django.shortcuts import render, redirect
from django.contrib import messages


def index(request):
    if request.session.get('contest'):
        del request.session['context']

    context = {}
    return render(request, 'survey/index.html', context)


def process_form(request):
    if request.session.get('contest'):
        del request.session['context']

    if request.method == 'GET':
        return redirect('/')

    if ((not request.POST.get('name')) or
            (not request.POST.get('location'))or
            (not request.POST.get('language'))):
        messages.add_message(request, messages.ERROR, 'validation failed')
        return redirect('/')

    if not request.session.get('attempts'):
        request.session['attempts'] = 1
    else:
        request.session['attempts'] += 1

    context = {
        'name': request.POST['name'],
        'location': request.POST['location'],
        'language': request.POST['language'],
        'comment': request.POST['comment'],
    }
    request.session['context'] = context

    return redirect('/result')


def result(request):
    try:
        context = request.session['context']
    except KeyError:
        return redirect('/')

    del request.session['context']
    return render(request, 'survey/result.html', context)
