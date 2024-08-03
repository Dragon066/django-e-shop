import logging

from cart.models import Cart
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import BadRequest
from django.db import transaction
from django.views.generic import FormView, ListView, TemplateView, UpdateView

from .forms import OrderForm
from .models import Order, OrderDetails


class MyOrdersView(LoginRequiredMixin, ListView):
    """
    A list of user's orders view.

    Displays a list of user's orders, the total amount of each order.

    Login required.
    """

    queryset = Order.objects.all()
    template_name = "my_orders.html"
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreateView(LoginRequiredMixin, FormView):
    """
    An order creation form view.

    Displays an order creation form and creates a new order
    if form is valid.

    Login required.
    """

    template_name = "order_create.html"
    form_class = OrderForm
    success_url = "/order/my_orders/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Cart.objects.filter(user=self.request.user)
        context["products"] = products
        summ = sum([item.product.price * item.quantity for item in products])
        context["summ"] = summ
        return context

    @transaction.atomic
    def form_valid(self, form):
        """
        Custom form validation function.

        Raises:
            BadRequest: If one of the products in the cart
            isn't available an error is thrown.
        """
        products = Cart.objects.filter(user=self.request.user)
        summ = sum([item.product.price * item.quantity for item in products])
        order = Order.objects.create(
            user=self.request.user,
            total_amount=summ,
            phone=form.cleaned_data["phone"],
            address=form.cleaned_data["address"],
        )
        for item in products:
            OrderDetails.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            item.delete()
            if not item.product.available:
                logging.warning(
                    f'Product {item.product} unavailable, order by "{self.request.user}" cancelled'
                )
                raise BadRequest(
                    f"Один из товаров ({item.product}) недоступен"
                )
            item.product.quantity -= item.quantity
            if item.product.quantity == 0:
                item.product.available = False
            item.product.save()

        logging.info(
            f'Order #{order.id} successfully created by "{self.request.user}"'
        )

        return super().form_valid(form)


class OrderDetailView(LoginRequiredMixin, TemplateView):
    """
    A detailed view of a specific user's order.

    Login required.
    """

    template_name = "order_detail.html"

    def get(self, request, pk):
        return self.render_to_response(self.get_context_data(pk=pk))

    def get_context_data(self, pk, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        order = Order.objects.get(pk=pk)
        products = OrderDetails.objects.filter(order=pk)
        context["order"] = order
        context["products"] = products
        return context


class OrderProcessView(LoginRequiredMixin, ListView):
    """
    A list of user's products orders from other users.

    Login required.
    """

    queryset = OrderDetails.objects.all().select_related("product")
    template_name = "order_process.html"
    paginate_by = 5

    def get_queryset(self):
        return OrderDetails.objects.filter(
            product__owner=self.request.user
        ).order_by("-order_id")


class OrderProcessDetailView(LoginRequiredMixin, UpdateView):
    """
    An order status update view.

    Displays an order status update form and updates an order status.

    Login required.
    """

    model = OrderDetails
    template_name = "order_process_detail.html"
    fields = ["status"]
    success_url = "/order/client_orders/"
