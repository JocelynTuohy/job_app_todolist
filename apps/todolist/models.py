# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, date
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from ..loginreg.models import User


class TodoManager(models.Manager):

    def allTodos(self, user):
        all_todos = (
            Todo.objects.filter(user=User.objects.get(id=user))
            .order_by('deadline')
        )
        return all_todos

    def addTodo(self, form_data, user_id):
        new_todo = Todo(
            user=User.objects.get(id=user_id),
            text=form_data['text'],
            deadline=datetime.strptime(form_data['deadline'], "%Y-%m-%d").date(),
            complete=False,
            details=form_data['details']
        )
        new_todo.save()
        return new_todo

    def validateTodo(self, form_data):
        errors = []
        # todo must have a description
        if len(form_data['text']) < 1:
            errors.append('Please provide a to-do description.')
        try:
            deadline = datetime.strptime(form_data['deadline'], "%Y-%m-%d").date()
            today = date.today()
        except ValueError:
            errors.append(
                'Invalid deadline date.'
            )
            return errors
        # date must be today or in the future
        if deadline < today:
            errors.append('You may not add to-dos with past deadlines.')
            return errors
        return errors


class Todo(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=100)
    deadline = models.DateField()
    complete = models.BooleanField(default=False)
    details = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TodoManager()