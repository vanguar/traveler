from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import login
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView


from .forms import *
from .models import *
from .utils import *


class Dir_travelHome(DataMixin, ListView):
    model = Dir_travel
    template_name = 'traveler/index.html'
    context_object_name = 'posts'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return  dict(list(context.items()) + list(c_def.items()))


    def get_queryset(self):
        return Dir_travel.objects.filter(is_published=True)


def about(request):
    contact_list = Dir_travel.objects.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'traveler/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'traveler/addpage.html'
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, oblect_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))



# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#
#     else:
#         form = AddPostForm()
#     return render(request, 'traveler/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'traveler/contact.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, oblect_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')

# def show_post(request, post_slug):
#     post = get_object_or_404(Dir_travel, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'traveler/post.html', context=context)

class ShowPost(DataMixin, DetailView):
    model = Dir_travel
    template_name = 'traveler/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, oblect_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title= context['post'])
        return dict(list(context.items()) + list(c_def.items()))

class Dir_travelCategory(DataMixin, ListView):
    model = Dir_travel
    template_name = 'traveler/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Dir_travel.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, oblect_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected = context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))


        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['menu'] = menu
        context['cat_selected'] = context['posts'][0].cat_id
        return context

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'traveler/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, oblect_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'traveler/login.html'

    def get_context_data(self, *, oblect_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')
