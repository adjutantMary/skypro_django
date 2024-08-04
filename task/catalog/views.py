import string

from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import VersionForm, ProductForm

import random

from .models import *


class ProductTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'product_list.html'

    def get(self, request, *args, **kwargs):
        self.extra_context = {
            "products": Product.objects.all(),
            "categories": Category.objects.all(),
        }
        return self.render_to_response(self.extra_context)


# class ProductListView(ListView):
#     model = Product
#     template_name = 'product_list.html'
#     content_object_name = 'object_list'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         for product in context['object_list']:
#             active_version = product.version_set.filter(is_current=True).first()
#             product.active_version = active_version
#         return context


class ProductDetailView(DetailView, LoginRequiredMixin):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_queryset(self, queryset=None):
        obj = super().get_queryset(queryset=queryset)
        obj.views += 1
        obj.save()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        active_version = product.version_set.filter(is_current=True).first()
        context['active_version'] = active_version
        return context


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


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')
    
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.owner != self.request.user:
            raise PermissionError
        return obj   
    

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
    
    def get_success_url(self) -> str:
        return reverse_lazy('product_list')


class VersionListView(ListView):
    model = Version
    template_name = 'version_list.html'
    context_object_name = 'versions'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        product = Product.objects.first()
        
        if product:
            product_id = product.pk
        else:
            product_id = None
        
        context['product_id'] = product_id
        
        return context
    

class VersionDetailView(DeleteView):
    model = Version
    template_name = 'version_detail.html'
    context_object_name = 'versions'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_id'] = kwargs['product_id']
        
        return context
    

class VersionCreateView(CreateView):
    model = Version
    fields = ['product', 'version_number', 'version_name', 'is_current']
    template_name = 'version_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        initial['product'] = self.kwargs['product_id']
        return initial
    

class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    fields = ['product', 'version_number', 'version_name', 'is_current']
    template_name = 'version_form.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('version')
    

class VersionDeleteView(DeleteView):
    model = Version
    template_name = 'version_confirm_delete.html'
    success_url = reverse_lazy('version_list.html')
    
    def get_success_url(self) -> str:
        return self.success_url

