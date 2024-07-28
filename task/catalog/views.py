import string

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

import random

from .models import *


class ProductTemplateView(TemplateView):
    template_name = 'product_list.html'

    def get(self, request, *args, **kwargs):
        self.extra_context = {
            "products": Product.objects.all(),
            "categories": Category.objects.all(),
        }
        return self.render_to_response(self.extra_context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class ContactView(TemplateView):
    template_name = 'contacts.html'

    def post(self, request, *args, **kwargs):
        print("Данные сохранены")
        return render(request, self.template_name)


class PostView(TemplateView):
    template_name = 'create_post.html'

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        published_posts = queryset.filter(status=Post.Status.PUBLISHED)
        return published_posts


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views += 1
        obj.save()
        return obj


class PostCreateView(CreateView):
    model = Post
    template_name = 'create_view.html'
    fields = ['title', 'content', 'preview', 'published']
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        random_slug = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=10))

        counter = 1
        new_slug = random_slug
        while Post.objects.filter(slug=new_slug).exists():
            new_slug = f'{random_slug}-{counter}'
            counter += 1

        instance.slug = new_slug

        instance.save()
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content', 'preview', 'published']
    context_object_name = 'post'
    slug_field = 'slug'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        return super().form_valid(form)


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post_list')

    def product_detail(self, request, pk):
        product = get_object_or_404(Product, **{'pk': pk})
        product.increment_views()
        context = {'product': product}
        return render(request, 'product_detail.html', context)
