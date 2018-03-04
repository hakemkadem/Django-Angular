from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

# admin.site.register(Book)
# admin.site.register(Author)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    list_filter = ('last_name','date_of_birth', 'first_name')
    fields = ['first_name','last_name', ('date_of_birth', 'date_of_death')]





@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status','borrower', 'due_back')
    list_filter = ('status', 'due_back')
    fieldsets = (
        ('Main Field', {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )





admin.site.register(Genre)


