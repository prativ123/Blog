from django import template
from ..models import Post
from django.db.models import Sum

register = template.Library()


@register.inclusion_tag('blogapp/latest_posts.html')
def show_latest_posts(count=3):
    latest_posts = Post.objects.order_by('-date_posted')[:count]
    return {'latest_posts': latest_posts}
    pass

@register.inclusion_tag('blogapp/most_viewed_posts.html')
def show_most_viewed_posts(count=3):
    most_viewed_posts = Post.objects.annotate(
                                    total_views=Sum('blog_views')
                                ).order_by('-total_views')[:count]
                                
    return {'most_viewed_posts' : most_viewed_posts}
    pass