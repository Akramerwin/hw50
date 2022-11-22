from django.shortcuts import render, reverse, redirect, get_object_or_404
from webapp.models import Todo
from webapp.forms import TodoForm
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

class TodoView(TemplateView):
    def get(self, request, *args, **kwargs):
       template_name = 'index.html'
       todo = Todo.objects.all()
       context = {
           'todo': todo
       }
       return render(request, template_name, context)


class View(TemplateView):
   template_name = 'todo_view.html'

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['todo'] = get_object_or_404(Todo, pk=kwargs['pk'])
       return context


class TodoCreate(View):
    def get(self, request, *args, **kwargs):
        form = TodoForm()
        return render(request, 'todo_create.html', {'form': form})
    def post(self, request, *args, **kwargs):
        form = TodoForm(data=request.POST)
        if form.is_valid():
            type = form.cleaned_data.pop('type')
            new_todo = Todo.objects.create(**form.cleaned_data)
            new_todo.type.set(type)
            return redirect('view', pk=new_todo.pk)
        else:
            return render(request, 'todo_create.html', {'form': form})

class UpdateTodo(View):
    def get(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        form = TodoForm(initial={
            'short_description': todo.short_description,
            'description': todo.description,
            'status': todo.status,
            'type': todo.type.all(),
        })
        return render(request, "todo_create.html", {'form': form})

    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        form = TodoForm(data=request.POST)
        if form.is_valid():
            todo.short_description = form.cleaned_data.get('short_description')
            todo.description = form.cleaned_data.get('description')
            todo.status = form.cleaned_data.get('status')
            todo.save()
            todo.type.set(form.cleaned_data['type'])
            return redirect('view', pk=todo.pk)
        else:
            return render(request, "todo_create.html", {'form': form})

class Delete(View):
    def get(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        return render(request, 'delete.html', context={'todo': todo})
    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk)
        todo.delete()
        return redirect('index')