from django.contrib import admin
from .models import Movies, Category, Review


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'categories_list')
    list_filter = ('categories',)


    def categories_list(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    categories_list.short_description = 'Categories'

admin.site.register(Movies, MovieAdmin)
admin.site.register(Category)
admin.site.register(Review)
