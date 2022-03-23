from django.contrib import admin


from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from backend.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'avatar', 'latitude',
                           'longitude', 'gender', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'avatar', 'is_staff', 'is_active',
                       'latitude', 'longitude', 'gender', 'first_name', 'last_name')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(User.user_like.through)