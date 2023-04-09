from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime, timedelta

from catalog.forms import RenewBookForm

# Create your views here.

def index(request):
	"""view function for home page of site"""
	
	
	# Generate count of some of the main objects
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()
	
	# Available books (status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()
	
	#The 'all()' is implied by default.
	num_authors = Author.objects.all().count()
	
	# Number of visits to this view, as counted in the session variable
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1
	
	
	
	
	context = {
		'num_books': num_books,
		'num_instances': num_instances,
		'num_instances_available': num_instances_available,
		'num_authors': num_authors,	
		'num_visits': num_visits,
	}
	
	# Render the HTML template index.html with the data in the context variable
	return render(request,'index.html', context=context)

class BookListView(generic.ListView):
	model = Book
	paginate_by = 10
	context_object_name = 'book_list' # your own name for the lista as a template variable
	queryset = Book.objects.filter(title__icontains='inverno')[:5] # Get 5 books containing the title inverno
	template_name = 'books/book_list.html' # Specify your own template name/location
	
	# opcao para substituir o queryset
	def get_queryset(self):
		return Book.objects.filter(title__icontains='inverno')[:5] # Get 5 books containing the title inverno
		
	
	# Alterando o contexto para inserir mais dados
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get the context
		context = super(BookListView, self).get_context_data(**kwargs)
		# Create any data and add it to the context
		context['some_data'] = 'This is just some data'

		return context
		
		
class BookDetailView(generic.DetailView):
	model = Book
	
	def book_detail_view(request, primary_key):
		book = get_object_or_404(Book, pk=primary_key)
		return render(request, 'catalog/book_detail.html', context={'book', book})	
		
		
class AuthorListView(generic.ListView):
	model = Author
	context_object_name = 'author_list'
	queryset = Author.objects.all()
	template_name = 'authors/author_list.html'
	
	
class AuthorDetailView(generic.DetailView):
	model = Author
	
	def author_detail_view(request, primary_key):
		author = get_object_or_404(Author, pk=primary_key)
		render(request, 'catalog/author_detail.html', context={'author', author})


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
	"""Generic class-based view listing books on loan to current user"""	
	permission_required = 'catalog.can_mark_returned'	
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginete_by = 10
	
	
	
	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksAllListView(LoginRequiredMixin, generic.ListView):
	"""Generic class-based view listing books on loan to current user"""		
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_all.html'
	paginete_by = 10
	
	permission_required = 'catalog.is_staff'
	
	def get_queryset(self):
		return BookInstance.objects.all().filter(status__exact='o').order_by('due_back')

	
	
def renew_book_librarian(request, pk):
	book_instance = get_object_or_404(BookInstance, pk=pk)
	
	# if this is a POST request then proceess the Form data
	if request.method == "POST":
		
		# Create a form instance and populate it with data from the request (binding)		
		form = RenewBookForm(request.POST)
		
		# Check if the form is valid:
		if form.is_valid():
			
			# process the data in form.cleaned_data as required (here we just write it to the model due_back field)
			book_instance.due_back = form.cleaned_data['renewal_date']	
			book_instance.save()
			
			# redirect to a new URL:
			return  HttpResponseRedirect(reverse('all-borrowed'))
			
	# if this is a GET (or any other method) create the default form.
	else:
		proposed_renewal_date = datetime.today() + timedelta(weeks=3)
		form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
		
	context = {
		'form': form,
		'book_instance': book_instance,
	}
	
	return render(request, 'catalog/book_renew_librarian.html', context)
	

