from django import forms
from phonenumber_field.formfields import PhoneNumberField, SplitPhoneNumberField
from .models import Order, Lottery


class LotteryForm(forms.ModelForm):
    
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'placeholder':'Lotería...'}), max_length=200, required=True)
    price = forms.FloatField(widget=forms.NumberInput())
    closing_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date', }), required=True)


    class Meta:
        model = Lottery
        fields = ("description", "image", "price", "closing_date", "closed")


class Order1Form(forms.ModelForm):
    quantity = forms.ChoiceField(
        widget=forms.Select(attrs={"onchange": "setAmount(this.value)"}),
        choices=[(x, x) for x in range(1, 11)],
        required=True,
    )
    dni = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Cédula"}),
        max_length=12,
        required=True,
    )
    type_of_dni = forms.ChoiceField(
        widget=forms.Select(), choices=Order.TYPE_OF_DNI, required=True
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Nro. de teléfono"}),
        max_length=11,
        min_length=11,
        required=True,
    )
    bank_code = forms.ChoiceField(
        widget=forms.Select(), choices=Order.BANK_CODE, required=True
    )
    reference = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Nro. de referencia"}),
        required=True,
        min_length=6,
    )
    amount_bs = forms.FloatField(
        widget=forms.NumberInput(attrs={"placeholder": "Monto", "readonly": ""}),
        required=True,
    )

    class Meta:
        model = Order
        fields = (
            "lottery",
            "user",
            "dollar",
            "payment_method",
            "quantity",
            "dni",
            "type_of_dni",
            "phone",
            "bank_code",
            "reference",
            "amount_bs",
        )


class Order2Form(forms.ModelForm):
    quantity = forms.ChoiceField(
        widget=forms.Select(attrs={"onchange": "setAmount(this.value)"}),
        choices=[(x, x) for x in range(1, 11)],
        required=True,
    )
    email_or_phone = forms.EmailField(
        widget=forms.TextInput(attrs={"placeholder": "Email o teléfono"}), required=True
    )
    amount_usd = forms.FloatField(
        widget=forms.NumberInput(attrs={"placeholder": "Monto", "readonly": ""}),
        required=True,
    )

    class Meta:
        model = Order
        fields = (
            "lottery",
            "user",
            "quantity",
            "payment_method",
            "email_or_phone",
            "amount_usd",
        )
