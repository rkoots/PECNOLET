from django import forms
from .models import Stock, Customer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class StockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput1 form-control'})
        self.fields['desc'].widget.attrs.update({'class': 'textinput1 form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput1 form-control', 'min': '0'})
        self.fields['type'].widget.attrs.update({'class': 'form-control'})
        self.fields['materials'].widget.attrs.update({'class': 'form-control'})
        self.fields['packing'].widget.attrs.update({'class': 'form-control'})
        self.fields['lotsize'].widget.attrs.update({'class': 'textinput1 form-control', 'min': '1'})
        self.fields['file'].widget.attrs.update({
            'class': 'custom-file-input',
            'accept': '.pdf,.doc,.docx,.jpg,.jpge,.png,.gif',
            'required': True
        })
        self.fields['is_deleted'].widget.attrs.update({'class': 'form-check-input'})

    class Meta:
        model = Stock
        fields = ['name', 'desc', 'quantity', 'type', 'materials', 'packing', 'lotsize', 'file', 'is_deleted']


class SelectCustomer(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Name'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['type_of_business'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['Address'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['EORI_number'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['VAT_number'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['is_deleted'].widget.attrs.update({'class': 'form-check-input'})

    class Meta:
        model = Customer
        fields = ['Name','type_of_business','Address','phone','email','EORI_number','VAT_number','is_deleted']

