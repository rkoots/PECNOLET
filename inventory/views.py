from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import (View, ListView, CreateView, UpdateView, DeleteView)
from django_filters.views import FilterView
from .filters import StockFilter, CustomerFilter
from .models import Stock, Customer, OutStock
from .forms import StockForm, SelectCustomer
from django.urls import reverse_lazy

class StockListView(FilterView):
    filterset_class = StockFilter
    queryset = Stock.objects.filter(is_deleted=False)
    template_name = 'inventory.html'
    paginate_by = 10

class StockCreateView(SuccessMessageMixin, CreateView):                                 # createview class to add new stock, mixin used to display message
    model = Stock                                                                       # setting 'Stock' model as model
    form_class = StockForm                                                              # setting 'StockForm' form as form
    template_name = "edit_stock.html"                                                   # 'edit_stock.html' used as the template
    success_url = '/inventory'                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "Stock has been created successfully"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Stock'
        context["savebtn"] = 'Add to Inventory'
        return context       

class StockUpdateView(SuccessMessageMixin, UpdateView):                                 # updateview class to edit stock, mixin used to display message
    model = Stock                                                                       # setting 'Stock' model as model
    form_class = StockForm                                                              # setting 'StockForm' form as form
    template_name = "edit_stock.html"                                                   # 'edit_stock.html' used as the template
    success_url = '/inventory'                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "Stock has been updated successfully"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Stock'
        context["savebtn"] = 'Update Stock'
        context["delbtn"] = 'Delete Stock'
        return context

class StockDeleteView(View):                                                            # view class to delete stock
    template_name = "delete_stock.html"                                                 # 'delete_stock.html' used as the template
    success_message = "Stock has been deleted successfully"                             # displays message when form is submitted
    def get(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        return render(request, self.template_name, {'object' : stock})
    def post(self, request, pk):  
        stock = get_object_or_404(Stock, pk=pk)
        stock.is_deleted = True
        stock.save()                                               
        messages.success(request, self.success_message)
        return redirect('inventory')

class CreateCustomer(SuccessMessageMixin, CreateView):
    model = Customer
    form_class = SelectCustomer
    success_url = '/'
    success_message = "Customer has been created successfully"
    template_name = "register_customer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Customer'
        context["savebtn"] = 'Add Customer'
        return context

def ViewProfileDetails(request):
    context = {}
    customer = Customer.objects.filter(user=request.user.id).first()
    context['customer'] = customer
    return render(request, 'profile.html', context)

class CustomerListView(ListView,FilterView):
    model = Customer
    filterset_class = CustomerFilter
    template_name = "customer/customer_list.html"
    queryset = Customer.objects.filter(is_deleted=False)
    paginate_by = 5

class CustomerCreateView(SuccessMessageMixin, CreateView):
    model = Customer
    form_class = SelectCustomer
    success_url = '/'
    success_message = "Customer has been created successfully"
    template_name = "customer/edit_customer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Customer'
        context["savebtn"] = 'Add Customer'
        return context

class CustomerUpdateView(SuccessMessageMixin, UpdateView):
    model = Customer
    form_class = SelectCustomer
    success_url = '/'
    success_message = "Customer details has been updated successfully"
    template_name = "customer/edit_customer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Customer'
        context["savebtn"] = 'Save Changes'
        context["delbtn"] = 'Delete Customer'
        return context

class CustomerDeleteView(View):
    template_name = "customer/delete_customer.html"
    success_message = "Customer Record has been deleted successfully"

    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        return render(request, self.template_name, {'object' : customer})

    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer.is_deleted = True
        customer.save()
        messages.success(request, self.success_message)
        return redirect('customers-list')

class CustomerView(View):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        return render(request, 'customer/customer.html', {'customer' : customer})


class OutStockCreateView(CreateView):
    model = OutStock
    fields = ['stock', 'quantity', 'remarks']
    template_name = 'outstock_form.html'
    success_url = reverse_lazy('inventory')

    def form_valid(self, form):
        stock = form.cleaned_data['stock']
        quantity = form.cleaned_data['quantity']

        if stock.quantity < quantity:
            form.add_error('quantity', 'Not enough stock available.')
            return self.form_invalid(form)

        return super().form_valid(form)