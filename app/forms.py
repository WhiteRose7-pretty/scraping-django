from django import forms


class BasicSearchForm(forms.Form):
    index = forms.CharField(max_length=250,
                            required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Indeks'}))
    name = forms.CharField(max_length=500,
                           required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Nazwa'}))
    ean = forms.CharField(max_length=100,
                          required=False,
                          widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'EAN'}))
    category = forms.CharField(max_length=50,
                               required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Kategoria'}))
    price_st = forms.DecimalField(max_digits=20,
                                  required=False,
                                  decimal_places=2,
                                  widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Cena od'}))
    price_end = forms.DecimalField(max_digits=20,
                                  required=False,
                                  decimal_places=2,
                                  widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Cena do'}))
    count_st = forms.IntegerField(required=False,
                               widget=forms.NumberInput(attrs={'class': 'form-control',
                                                               'placeholder': 'Ilość od'}))
    count_end = forms.IntegerField(required=False,
                               widget=forms.NumberInput(attrs={'class': 'form-control',
                                                               'placeholder': 'Ilość do'}))
