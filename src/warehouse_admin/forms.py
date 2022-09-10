from django import forms
from django.forms import ModelForm
from main.models import Batch, ItemCard, ItemType, Distributor, RetailCard, RetailItem

class DateInput(forms.DateInput):
    input_type = 'date'

class AddGoodsForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddGoodsForm, self).__init__(*args, **kwargs)
        
        types = []
        ItemTypes = ItemType.objects.filter(is_retail=False)
        for i in ItemTypes:
                types.append((f'{i}', f'{i}'))

        widget = forms.Select(attrs={'required': True, 'class': 'form-control'})
        self.fields['type'] = forms.ChoiceField(choices=types, widget=widget)

    class Meta:
        model = ItemCard
        fields = [
            'batch',
            'quantity',
            'received_from',
        ]
        widgets = {
            'batch': forms.Select(attrs={'required': True, 'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Quantity'}),
            'received_from': forms.TextInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Received From'}),
        }

class RegisterItemForm(ModelForm):
    class Meta:
        model = ItemType
        fields = [
            'name',
            'code',
            'weight',
            'is_retail'            
        ]
        widgets = {
            'name': forms.TextInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Name'}),
            'code': forms.TextInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Code'}),
            'weight': forms.TextInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Received From'}),
            'is_retail': forms.CheckboxInput()
        }

class AddBatchForm(ModelForm):
    class Meta:
        model = Batch
        fields = [
            'name',
            'code',
            'arrival_date',
            'quantity',
            'description',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Name'}),
            'code': forms.TextInput(attrs={'required': False, 'class': 'form-control', 'placeholder': 'Code'}),
            'arrival_date': DateInput(attrs={'required': False, 'class': 'form-control', 'data-provide':'datepicker'}),
            'quantity': forms.NumberInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Quantity'}),
            'description': forms.Textarea(attrs={'required': False, 'class': 'form-control', 'placeholder': 'Description'}),
        }

class SendGoodsForm(ModelForm):
    def __init__(self, pk=1, *args, **kwargs):
        super(SendGoodsForm, self).__init__(*args, **kwargs)
        items, batches, dis, status= [], [], [], [
                                                  ('Good', 'Good'),
                                                  ('Damaged', 'Damaged')]
        if pk != 1: 
            dis.append(('Main Storage', 'Main Storage'))
        for i in Distributor.objects.all():
            if i.stock.id != int(pk):
                dis.append((f'{i.person.name}', f'{i.person.name}'))
        stock = ItemCard.objects.filter(stock=pk)
        for i in stock:
            if (f'{i.type}', f'{i.type}') not in items: 
                items.append((f'{i.type}', f'{i.type}'))
            if (f'{i.batch}', f'{i.batch}') not in batches: 
                batches.append((f'{i.batch}', f'{i.batch}'))
        widget = forms.Select(attrs={'required': True, 'class': 'form-control'})
        widget2 = forms.Select(attrs={'required': False, 'class': 'form-control'})
        self.fields['type'] = forms.ChoiceField(choices=items, widget=widget)
        self.fields['batch'] = forms.ChoiceField(choices=batches, widget=widget)
        self.fields['status'] = forms.ChoiceField(choices=status, widget=widget2)
        self.fields['send_to'] = forms.ChoiceField(choices=dis, widget=widget2)

    class Meta:
        model = ItemCard
        fields = [
            'quantity',
        ]
        widgets = {
            'quantity': forms.NumberInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Quantity'}),
        }

class ConvertToRetailForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ConvertToRetailForm, self).__init__(*args, **kwargs)
        items, batches= [], []
        stock = ItemCard.objects.filter(stock=1)
        for i in stock:
            if not i.type.is_retail and (f'{i.type}', f'{i.type}') not in items: 
                items.append((f'{i.type}', f'{i.type}'))
            if (f'{i.batch}', f'{i.batch}') not in batches: 
                batches.append((f'{i.batch}', f'{i.batch}'))
        widget = forms.Select(attrs={'required': True, 'class': 'form-control'})
        self.fields['type'] = forms.ChoiceField(choices=items, widget=widget)
        self.fields['batch'] = forms.ChoiceField(choices=batches, widget=widget)

    class Meta:
        model = ItemCard
        fields = [
            'quantity',
        ]
        widgets = {
            'quantity': forms.NumberInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Quantity'}),
        }
    
class AddRetailGoodsForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddRetailGoodsForm, self).__init__(*args, **kwargs)
        
        types = []
        ItemTypes = ItemType.objects.filter(is_retail=True)
        for i in ItemTypes:
                types.append((f'{i}', f'{i}'))

        widget = forms.Select(attrs={'required': True, 'class': 'form-control'})
        self.fields['type'] = forms.ChoiceField(choices=types, widget=widget)

    class Meta:
        model = RetailItem
        fields = [
            'quantity',
        ]
        widgets = {
            'quantity': forms.NumberInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Quantity'}),
        }
