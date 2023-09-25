from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
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


from taggit.models import Tag

def post_list(request, tag_slug=None):
    posts = Post.objects.all()

    # post tag
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag]).order_by('-date_posted')
    
    # Define paginator and page number outside of the if statement
    paginator = Paginator(posts, 3)  # Show 3 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Pass is_paginated flag to template context
    is_paginated = page_obj.has_other_pages()
    
    return render(request, 'blogapp/post_list.html', {'tag': tag, 'page_obj': page_obj, 'is_paginated': is_paginated})




class UserPostListView(ListView):
    model = Post
    template_name = 'blogapp/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



from django.db.models import Count

class PostDetailView(DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        
        # Increment the view count by 1
        obj.blog_views += 1
        obj.save()

        return super().get(request, *args, **kwargs)
    # comment = Comment.objects.filter(post=comment).order_by('-id')[:7]

    # def get_queryset(self):
    #     comment = get_object_or_404(Post, comment=self.kwargs.get('comment'))
    #     return Comment.objects.filter(post=comment).order_by('-date_posted')[:7]
    # ordering = ['posted_on']
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        
        post = self.get_object()
        comments = Comment.objects.filter(post=post).order_by('-date_posted')[:7]
        data['comments'] = comments

        likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked

        # Retrieving list of similar articles
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(tags__in=post_tags_ids)\
                                        .exclude(id=post.id)
        similar = similar_posts.annotate(same_tags_in_article=Count('tags'))\
                                        .order_by('-same_tags_in_article','-date_posted')[:3]
        data['similar'] = similar 
        return data
    
                

    
    
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.shortcuts import render,redirect

@login_required
def add_comment(request: HttpRequest,post_id)->HttpResponse:
    if request.method == "POST":
        user = request.user
        posts = Post.objects.get(id=post_id)

        comment = request.POST.get("comment","").strip()
        if comment:
            new_comment = Comment(user=user, post=posts, comment=comment)
            new_comment.save()
            messages.success(request, "Thank you for your comment!")
        else:
            messages.success(request, "Comment cannot be empty.")

    return redirect('post-detail', pk=post_id)

from django import forms
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    
    fields = ['title', 'content', 'image', 'tags']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'tags']


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

from django.shortcuts import HttpResponseRedirect

def PostLike(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


