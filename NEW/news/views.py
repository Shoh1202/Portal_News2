from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,  TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post,  Author
from .my_filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
class PostList(ListView):
    model=Post
    ordering='-time_add'
    template_name='news/news_list.html'
    context_object_name ='news_list'
    paginate_by = 1

class PostSearch(ListView):
    model = Post
    ordering = "-time_add"
    template_name = "news/news_search.html"
    context_object_name = "news_list"
    paginate_by = 1
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
class DetailPost(DetailView):
    model=Post
    template_name = "news/news_detail.html"
    context_object_name = "news"
class PostCreate(LoginRequiredMixin,CreateView):
    form_class =PostForm
    model = Post
    post_type_value = Post.PostType.NEWS
    template_name ='news/news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        author = Author.objects.get_or_create(user=self.request.user)[0]
        post.author = author
        post.post_type = self.post_type_value
        post.save()
        form.save_m2m()
        return super().form_valid(form)
class PostUpdate(LoginRequiredMixin,UpdateView):
    form_class =PostForm
    model = Post
    template_name ='news/news_create.html'

    def dispatch(self, request, *args, **kwargs):

        post = self.get_object()


        if post.author.user != request.user:
            return redirect('news')

        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        return Post.objects.filter(post_type=Post.PostType.NEWS)
class PostDelete(LoginRequiredMixin,DeleteView):
    model = Post
    template_name='news/news_delete.html'
    success_url = reverse_lazy('news')

    def dispatch(self, request, *args,  **kwargs):
        post = self.get_object()

        if post.author.user != request.user:
            return redirect('news')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.filter(post_type=Post.PostType.NEWS)
class PostCreate1( CreateView):
    form_class =PostForm
    model = Post
    post_type_value = Post.PostType.ARTICLE
    template_name ='news/ARTICLE_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)

        post.post_type = self.post_type_value
        post.save()
        form.save_m2m()
        return super().form_valid(form)
class PostUpdate1(LoginRequiredMixin,UpdateView):
    form_class =PostForm
    model = Post
    template_name ='news/Article_create.html'

    def dispatch(self, request, *args, **kwargs):
        post=self.self.get_object()
        if post.author != request.user:
            return redirect('news')
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        return Post.objects.filter(post_type=Post.PostType.ARTICLE)


class PostDelete1(LoginRequiredMixin,DeleteView):
    model = Post
    template_name='news/Article_delete.html'
    success_url = reverse_lazy('news')
    def dispatch(self, request, *args, **kwargs):
        post=self.self.get_object()
        if post.author != request.user:
            return redirect('news')
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        return Post.objects.filter(post_type=Post.PostType.ARTICLE)

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'news/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context
