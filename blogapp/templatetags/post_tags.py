from django import template
from ..models import Post

register = template.Library()


@register.inclusion_tag('blogapp/latest_posts.html')
def show_latest_posts(count=3):
    latest_posts = Post.objects.order_by('-date_posted')[:count]
    return {'latest_posts': latest_posts}
    pass