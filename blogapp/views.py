from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import *
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

# from django.http import HttpResponse
# Create your views here.


def home(request):
    context={
        'posts':Post.objects.all()
    }
    return render(request, 'blogapp/home.html',context)


class PostListView(ListView):
    model = Post
    template_name = 'blogapp/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blogapp/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    
from django.db.models import Q
from django.core.paginator import Paginator

def search_feature(request):
    if request.method == 'GET':
        # Retrieve the search query entered by the user
        search_query = request.GET['search_query']
        
        # Filter your model by the search query
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(author__username__icontains=search_query)).order_by('-date_posted')
        
        # Configure pagination
        paginator = Paginator(posts, 5)  # Show 5 posts per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Pass is_paginated flag to template context
        is_paginated = page_obj.has_other_pages()
        
        return render(request, 'blogapp/search_post.html', {'query': search_query, 'page_obj': page_obj, 'is_paginated': is_paginated})
    else:
        return render(request, 'blogapp/search_post.html', {})


# class SearchPostListView(ListView):
#     model = Post
#     template_name = 'blogapp/search_post.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'posts'
#     paginate_by = 5
#     search_query = request.POST['search_query']

#     def get_queryset(self):
#         user = get_object_or_404(User, username=self.kwargs.get('username'))
#         return Post.objects.filter(author=user).order_by('-date_posted')


def about(request):
    return render(request, 'blogapp/about.html')