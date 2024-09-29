from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'phone', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {'fields': ('date_of_birth', 'bio', 'photo', 'job', 'phone')}),
    )



#این فانکشن برای اکشن نویسی در قسمت ادمین میباشد
def make_deactivation(modeladmin,request,queryset):
    result=queryset.update(active=False)
    modeladmin.message_user(request,f"{result} posts were rejected")

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    
    list_display=["author", 'created', 'description']
    search_fields=["description"]
    ordering=["created"]
    actions=[make_deactivation]
    
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'created', 'active']
    list_filter = ['active', 'created','updated',]
    search_fields = ['name', 'body']
    list_editable = ['active']
    

admin.site.register(Contact)
admin.site.register(Image)