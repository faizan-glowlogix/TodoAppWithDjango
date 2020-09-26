from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import *
from .forms import *
# Create your views here.

def index(request):
    tasks = Task.objects.all()
    
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            
            html_content = render_to_string('email_template.html',
            {'title':'New Task Added','line':'A New Task has been added','content':form['title'].value()})
            print(html_content)
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                'New Task Added',
                text_content,
                'admin@example.com',
                ['faizan@example.com'],
            )
            email.attach_alternative(html_content,"text/html")
            print(form['title'].value())
            email.send()
            # send_mail(
            #     'New Task Added',
            #     'A new Task is Added',
            #     'admin@example.com',
            #     ['faizan@example.com'],
            #     fail_silently = False)
        return redirect('/')


    
    context = {'tasks':tasks, 'form':form}
    return render(request,'tasks/list.html', context)

def updateTask(request, pk):

    task = Task.objects.get(id=pk)

    form = TaskForm(instance=task)

    context={'form':form}
    
    if request.method == 'POST':
        form = TaskForm(request.POST , instance=task)
        if form.is_valid():
            form.save()
            html_content = render_to_string('email_template.html',
            {'title':'Task Updated','line':'A Task has been updated','content':form['title'].value()})
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                'Task Updated',
                text_content,
                'admin@example.com',
                ['faizan@example.com'],
            )
            email.attach_alternative(html_content,"text/html")
            email.send()
        return redirect('/')

    
    return render(request, 'tasks/update_task.html',context)

def deleteTask(request,pk):
    item = Task.objects.get(id=pk)

    if request.method == 'POST':
        html_content = render_to_string('email_template.html',
            {'title':'Task Deleted','line':'A Task has been deleted','content':item.title})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            'Task Deleted',
            text_content,
            'admin@example.com',
            ['faizan@example.com'],
        )
        email.attach_alternative(html_content,"text/html")
        email.send()
        item.delete()
        return redirect('/')

    context= {'item':item}
    return render(request,'tasks/delete.html',context)