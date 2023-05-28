from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms

from users.models import User, UserType


class UserChangeForm(forms.ModelForm):
    """ Form for change user password """
    password = ReadOnlyPasswordHashField(label="Password",
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = User
        fields = ('password', )

    def clean_password(self):
        return self.initial["password"]


@admin.register(User)
class UserAdmin(ModelAdmin):
    """ User settings for admin panel """
    form = UserChangeForm
    fieldsets = (
        (None, {
            'fields': ('email', 'name', 'surname', 'user_type')
        }),
        ('Advanced options', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'password'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'name', 'surname', 'user_type', 'is_superuser')
    ordering = ('email', 'is_superuser')
    search_fields = ['email', 'name', 'surname', 'user_type']


@admin.register(UserType)
class UserTypeAdmin(ModelAdmin):
    """ admin panel for user type """
    fields = ['name', 'code']
