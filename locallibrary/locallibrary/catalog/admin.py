from django.contrib import admin
from catalog.models import Author, Genre, Book, BookInstance

# Register your models here.

#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(BookInstance)


class AuthorAdmin(admin.ModelAdmin):
	list_diplay = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
	fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
admin.site.register(Author, AuthorAdmin)


#Register the Admin for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'display_genre')
	
#Register the Admin for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
	list_filter = ('book','status','borrower', 'due_back','id')
	
	fieldsets = (
		(None, {
			'fields': ('book','imprint','id')
		}),
		('Availability', {
			'fields': ('status','due_back','borrower')
		}),
	)

