from django.shortcuts import render
from posts.models import Post
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView, DeleteView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)

# def home(request):
#     context = {
#         'all_posts': Post.objects.all()
#     }
#     return render(request, 'posts/index.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'all_posts'
    ordering = '-date'


class PostDetailView(DetailView):
    model = Post
    # fields = ['title', 'content', 'image']



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
        print(post.author)
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




def about(request):
    return render(request, 'posts/about.html')
