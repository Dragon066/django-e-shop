from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, FormView, View
from .models import Cart
from .forms import CartForm
from catalog.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin


class CartView(LoginRequiredMixin, ListView):
    queryset = Cart.objects.all()
    template_name = 'cart.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).select_related('product')
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        data = self.get_queryset()
        summ = sum([item.product.price * item.quantity for item in data])
        context['summ'] = summ
        return context


class CartFormView(LoginRequiredMixin, FormView):
    form_class = CartForm
    template_name = 'cart_detail.html'
    success_url = '/catalog/'

    def get_initial(self):
        initial = super().get_initial()
        product_id = self.request.path.split('/')[-1]
        try:
            quantity = Cart.objects.filter(user=self.request.user, product__id=product_id).first().quantity
        except:
            quantity = 1
        initial['quantity'] = quantity
        return initial

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if 'delete_cart' in request.POST:
            cart = Cart.objects.filter(user=self.request.user, product__id=request.POST.get('product_id'))
            cart.delete()
            return HttpResponseRedirect(self.get_success_url())
        if form.is_valid():
            product_id = request.POST.get('product_id')
            max_quantity = Product.objects.get(pk=product_id).quantity
            if form.cleaned_data['quantity'] > max_quantity:
                return self.form_invalid(form, product_id)
            form.cleaned_data['product_id'] = product_id
            form.cleaned_data['user'] = request.user
            return self.form_valid(form)
        else:
            return self.form_invalid(form, product_id)

    def form_valid(self, form):
        product = Product.objects.get(pk=form.cleaned_data['product_id'])
        Cart.objects.update_or_create(user=form.cleaned_data['user'], 
                            product=product,
                            defaults={'quantity': form.cleaned_data['quantity']})
        return super().form_valid(form)
    
    def form_invalid(self, form, pk):
        form.add_error('quantity', 'Превышает максимальное количество')
        return self.render_to_response(self.get_context_data(form=form, pk=pk))
    
    def get(self, request, pk):
        return self.render_to_response(self.get_context_data(pk=pk))
    
    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk', None)
        context = super().get_context_data(**kwargs)
        if pk:
            product = Product.objects.get(pk=pk)
            context['product'] = product
        if Cart.objects.filter(user=self.request.user, product__id=pk).first():
            context['exists'] = True
        return context
    

class CartDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=self.request.user, product__id=kwargs.get('pk')).first()
        cart.delete()
        return HttpResponseRedirect('/cart/')
