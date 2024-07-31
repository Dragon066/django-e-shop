
from cart.models import Cart
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import (
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import ProductForm
from .models import Product


class ProductListView(ListView):
    queryset = Product.objects.filter(available=True)
    template_name = "catalog_list.html"
    paginate_by = 10

    def get_queryset(self):
        ascending = self.request.GET.get("asc", "1")
        order = self.request.GET.get("order", "name")
        return (
            super()
            .get_queryset()
            .order_by(f'{"" if ascending == '1' else "-"}{order}')
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        ascending = self.request.GET.get("asc", "1")
        order = self.request.GET.get("order", "name")
        page = self.request.GET.get("page", "1")
        context["asc"] = ascending
        context["order"] = order
        context["page_number"] = page
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).select_related(
                "product"
            )
            context["cart"] = list(map(lambda x: x.product, cart))

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        ascending = self.request.GET.get("asc", "1")
        order = self.request.GET.get("order", "name")
        page = self.request.GET.get("page", "1")
        context["asc"] = ascending
        context["order"] = order
        context["page_number"] = page
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.available and self.object.owner != request.user:
            raise Http404("Товар не найден")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ContactsView(TemplateView):
    template_name = "contacts.html"


class ProductFormView(LoginRequiredMixin, FormView):
    template_name = "create_product.html"
    form_class = ProductForm
    success_url = "/catalog/my_products/"

    def form_valid(self, form):
        temp = form.save(commit=False)
        temp.owner = self.request.user
        temp.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = (
        "name",
        "description",
        "price",
        "quantity",
        "category",
        "picture",
        "available",
    )
    success_url = "/catalog/my_products/"
    template_name = "create_product.html"


class ProductUserListView(LoginRequiredMixin, ListView):
    queryset = Product.objects.all()
    template_name = "my_products.html"
    paginate_by = 10

    def get_queryset(self):
        ascending = self.request.GET.get("asc", "1")
        order = self.request.GET.get("order", "name")
        return (
            super()
            .get_queryset()
            .filter(owner=self.request.user)
            .order_by(f'{"" if ascending == '1' else "-"}{order}')
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        ascending = self.request.GET.get("asc", "1")
        order = self.request.GET.get("order", "name")
        page = self.request.GET.get("page", "1")
        context["asc"] = ascending
        context["order"] = order
        context["page_number"] = page

        return context
