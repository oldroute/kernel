from django.shortcuts import render


def book_admin(request):
    template = 'admin/book.html'
    extra_context = {}
    return render(request, template, extra_context)