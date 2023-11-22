from typing import Any
from django import forms
from .models import Product,Profile


class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields='__all__'

    image=forms.ImageField(widget=forms.FileInput)

       
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class']="form-control"
        self.fields['name'].widget.attrs['placeholder']="Enter name of the product"   
        self.fields['price'].widget.attrs['class']="form-control"
        self.fields['price'].widget.attrs['placeholder']="Enter price of the product"   
        self.fields['digital'].widget.attrs['class']="form-control"
        self.fields['image'].widget.attrs['class']="form-control"  


class Profileform(forms.ModelForm):
    class Meta:
        model=Profile
        fields='__all__'
        exclude=['name']

    image=forms.ImageField(widget=forms.FileInput)

       
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(Profileform,self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class']="form-control"
        self.fields['email'].widget.attrs['placeholder']="Enter your email"
        self.fields['address'].widget.attrs['class']="form-control"
        self.fields['address'].widget.attrs['placeholder']="Enter your address"  
        self.fields['phone'].widget.attrs['class']="form-control"
        self.fields['phone'].widget.attrs['placeholder']="Enter your phone"
        self.fields['image'].widget.attrs['class']="form-control"  