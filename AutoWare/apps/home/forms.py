from django import forms
from apps.authentication.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Product
# For Manager 
class ManagerForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
        'id': 'name',
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address',
        'data-val': 'true',
        'data-val-required': 'Please enter address',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'type': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'data-val': 'true',
        'data-val-required': 'Please enter username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'data-val': 'true',
        'data-val-required': 'Please enter password',
    }))
    retype_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'retype_password',
        'data-val': 'true',
        'data-val-required': 'Please enter retype_password',
    }))
    
# For User Profile
class UserForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'type': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'data-val': 'true',
        'data-val-required': 'Please enter username',
        'readonly': 'readonly',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'data-val': 'true',
        'data-val-required': 'Please enter password',
    }))
    retype_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'retype_password',
        'data-val': 'true',
        'data-val-required': 'Please enter retype_password',
    }))
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control btn btn-primary btn-sm',
            'id': 'image',
            'data-val': 'true',
            'data-val-required': 'Please upload your image',
            'type': 'file',
        }),
        required=False
        )
    
    
# For Notification
class NotificationForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
        'id': 'name',
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    message = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address',
        'data-val': 'true',
        'data-val-required': 'Please enter address',
    }))
    # Admin,Manager
    ASSIGNED_CHOICES = (
        ('1', 'Manager'),
        ('2', 'Warehouse Team'),
        ('3', 'Operations Team'),
        ('4', 'Suppliers'),
    )
    assigned_to = forms.ChoiceField(
        choices=ASSIGNED_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'assigned_to',
            'data-val': 'true',
            'data-val-required': 'Please select at least one user',
            
        }),required=False
        )
    choices_opteams = (
        ('1', 'Managers'),
        ('2', 'Warehouse Team'),
    )
    assigned_op = forms.ChoiceField(
        choices=choices_opteams,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'assigned_op',
            'data-val': 'true',
            'data-val-required': 'Please select at least one user',
            
        }),required=False
        )
    choices_warteams = (
        ('1', 'Managers'),
        ('3', 'Operations Team'),
    )
    assigned_war = forms.ChoiceField(
        choices=choices_warteams,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'assigned_war',
            'data-val': 'true',
            'data-val-required': 'Please select at least one user',
            
        }),required=False
        )
    choices_sup = (
        ('1', 'Managers'),
        ('2', 'Warehouse Team'),
    )
    assigned_sup = forms.ChoiceField(
        choices=choices_sup,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'assigned_sup',
            'data-val': 'true',
            'data-val-required': 'Please select at least one user',
            
        }),required=False
        )

    STATUS_CHOICES = (
        ('1', 'Open'),
        ('0', 'Closed'),
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'status',
            'data-val': 'true',
            'data-val-required': 'Please select a status',
        })
    )

# For Employee
class EmpForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
        'id': 'name',
        'data-val': 'true',
        'data-val-required': 'Please enter name',
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address',
        'data-val': 'true',
        'data-val-required': 'Please enter address',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'type': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'data-val': 'true',
        'data-val-required': 'Please enter username',
    }))
    Team_CHOICES = (
        ('1', 'Warehouse Team'),
        ('0', 'Operations Team'),
    )
    team = forms.ChoiceField(
        choices=Team_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'team',
            'data-val': 'true',
            'data-val-required': 'Please select a team',
        })
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'data-val': 'true',
        'data-val-required': 'Please enter password',
    }))
    retype_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'retype_password',
        'data-val': 'true',
        'data-val-required': 'Please enter retype_password',
    }))
    
class SupReqForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
        'id': 'name',
        'data-val': 'true',
        'data-val-required': 'Please enter product name',
    }))
    desp = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
        'id': 'desp',
        'data-val': 'true',
        'data-val-required': 'Please enter description',
    }))
    Status = (
        ('1', 'Accepted'),
        ('2', 'In-Progress'),
        ('0', 'Declined'),
    )
    status = forms.ChoiceField(
        choices=Status,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'status',
            'data-val': 'true',
            'data-val-required': 'Please select a status',
        }),required=False
    )
    quantity = forms.IntegerField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'quantity',
            'data-val': 'true',
            'data-val-required': 'Please enter quantity',
        }),
        validators=[MinValueValidator(1), MaxValueValidator(15000)]
    )
    quote = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'quote',
            'data-val': 'true',
            'data-val-required': 'Please enter quote',
        })
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control btn btn-primary btn-sm',
            'id': 'image',
            'data-val': 'true',
            'data-val-required': 'Please upload an image',
            'type': 'file',
        })
        )
    
class ReqForm(forms.Form):
    # name = forms.ModelChoiceField(queryset=Product.objects.values_list('name' ,flat=True).distinct(), empty_label="Select a product", widget=forms.Select(attrs={
    #     'class': 'form-control',
    #     'id': 'name',
    #     'data-val': 'true',
    #     'data-val-required': 'Please select a product',
    # }))
    Status = (
        ('1', 'Accepted'),
        ('2', 'In-Progress'),
        ('0', 'Declined'),
    )
    status = forms.ChoiceField(
        choices=Status,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'status',
            'data-val': 'true',
            'data-val-required': 'Please select a status',
        }),required=False
    )
    quantity = forms.IntegerField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'quantity',
            'data-val': 'true',
            'data-val-required': 'Please enter quantity',
        }),
        validators=[MinValueValidator(1), MaxValueValidator(50)]
    )

class AddProductForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'text',
        'id': 'name',
        'data-val': 'true',
        'data-val-required': 'Please enter product name',
    }))