from django.shortcuts import render
from .models import Book,BookInstance,Author,Genre,FileCode
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse;
from django.core import serializers;
from django.http import HttpResponse;
import json;

def Valid_Author(request):
    authName=request.GET.get('authName',None);
    num_books = Book.objects.all().count()
    num_visits = request.session.get('num_visits', 0);
    request.session['num_visits'] = num_visits + 1;
    data  ={
            'num_visits':num_visits
    }
    return JsonResponse(data)

def GetFileCode(request):
    # FileCode = request.GET.get('authName',None);
    if request.method == 'POST':
        Groups=list(json.loads(request.POST.get('deal',None)))
        for i in range(len(Groups)):
            bo=Book(title=Groups[i]['title'],
                    summary=Groups[i]['summary'],
                    isbn=Groups[i]['isbn'],
                    author_id=Groups[i]['author_id'])
            TestExist = Book.objects.filter(title__exact=Groups[i]['title']).count();
            if(TestExist==0):
                 bo.save();
        # Groups = Genre.objects.filter(id__exact=1).update(title=FileCode);
        Groups=Book.objects.all();
        lists=[1,2,3,4]
        # Groups_serialized = serializers.serialize('json', Groups)
        data =Groups;
    return HttpResponse(serializers.serialize("json", data),
                        content_type='application/json')


class BookListView(LoginRequiredMixin,generic.ListView):
    model = Book
class BookDetailView(LoginRequiredMixin,generic.DetailView):
    model = Book
class AuthorListView(generic.ListView):
    model = Author;
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(AuthorListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['MyBooks'] =Book.objects.all()
        return context

    template_name = 'Catalog/Author_list.html'
class AuthorDetailView(generic.DetailView):
    model = Author;
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['MyBooks'] = Book.objects.filter(author__last_name__contains='kanabi');
        return context

    template_name = 'Catalog/Author_detail.html'

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
        """
        Generic class-based view listing books on loan to current user.
        """
        model = BookInstance
        template_name = 'Catalog/bookinstance_list_borrowed_user.html'
        paginate_by = 10

        def get_queryset(self):
            return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by(
                'due_back')
# Create your views here.
def Catalog_list(requst):
    return render(requst,'Catalog/Catalog_list.html');
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.all().count()  # The 'all()' is implied by default.
    BookPerAuthor=Book.objects.all().filter(author__last_name__contains='kanabi');
    num_visits = request.session.get('num_visits',0);
    request.session['num_visits'] =num_visits+1;
    return render(
        request,
        'Catalog/index.html',
        context ={
            'num_visits':num_visits,
            'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},
    )


from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime


from .forms import RenewBookForm
@permission_required('Catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html',
                  {'form': form,
                   'bookinst':book_inst})

