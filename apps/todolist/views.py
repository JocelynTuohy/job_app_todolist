# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from datetime import datetime, date
from .models import Todo
from ..loginreg.models import User

# Create your views here.
def index(request):
    print('in the todolist index route')
    logged_user = User.objects.get(id=request.session['id'])
    context = {
        'user': logged_user,
        'all_todos': Todo.objects.allTodos(request.session['id']),
        'today': date.today()
    }
    return render(request, 'todolist/index.html', context)

def add(request):
    print('in the todolist add route')
    if request.method == 'POST':
        errors = Todo.objects.validateTodo(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect(reverse('todolist:index'))
        else:
            Todo.objects.addTodo(request.POST, request.session['id'])
    return redirect(reverse('todolist:index'))

def more(request, todo):
    print('in the todolist more route')
    context = { 'todo': Todo.objects.get(id=todo) }
    return render(request, 'todolist/more.html', context)

def delete(request, todo):
    print('in the todolist delete route')
    try:
        Todo.objects.get(id=todo).delete()
    except ObjectDoesNotExist:
        messages.error(request, 'You just tried to delete a to-do ' +
                       'that does not exist.')
    return redirect(reverse('todolist:index'))

def complete(request, todo):
    print('in the todolist complete route')
    this_todo = Todo.objects.get(id=todo)
    if this_todo.complete == False:
        this_todo.complete = True
        this_todo.save()
    else:
        this_todo.complete = False
        this_todo.save()
    return redirect(reverse('todolist:index'))