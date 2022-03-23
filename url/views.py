from urllib.parse import urlparse

from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View, CreateView, DeleteView

from .forms import *
from .models import *


# Create your views here.

class Index(TemplateView):
    template_name = 'index.html'


class AccountView(TemplateView):
    template_name = "account/account.html"


class AccountCreation(CreateView):
    template_name = "account/create.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


class URLCreate(View):
    template_name = "urls/create.html"
    model = URL

    # this should not be a normal create view, this should be something else
    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name, {})

    @method_decorator(login_required)
    def post(self, request):
        """
        User posts the data through a fetch request, and redirects themselves to the account page.
        Creates a new URL
        """

        # This should take the data the user has and create a new url
        dests = request.headers['destinations'].split(",")
        probs = request.headers['probs'].split(",")  # str > string list

        # Creates model objects for each destination
        assert len(dests) == len(probs), "Destinations not the same length"
        destinations = [Destination.objects.create(views=0, url=dests[i], prob=float(probs[i])) for i in
                        range(len(dests))]

        for item in destinations:  # just saves everything
            item.save()

        # Creates a new url object
        url = URL.objects.create(title=request.headers['title'], owner=request.user)
        url.set_link_string()
        for item in destinations:
            url.destinations.add(item)
        print("Created URL with link string: ", url.link_string)
        url.save()

        return HttpResponseRedirect(reverse_lazy('account-view'))


class URLDelete(DeleteView):
    model = URL
    success_url = reverse_lazy('account-view')
    template_name = "urls/delete.html"


class URLEdit(View):
    template_name = "urls/edit.html"

    # This should be almost exactly the same as create, except, there should be an intial value passed in for the urls

    # The backend shoudl match new and old urls so the viewcounts do not change

    # The view should show the user when things have changed

    @method_decorator(login_required)
    def get(self, request, link_string):
        url = self.get_url(link_string)

        if url is None or request.user != url.owner:
            return HttpResponseRedirect(reverse_lazy('index'))

        return render(request, self.template_name, {'url': url})

    @method_decorator(login_required)
    def post(self, request, link_string):
        url = self.get_url(link_string)

        if url is None or request.user != url.owner:  # Only the owner can edit the string
            return HttpResponseRedirect(reverse_lazy('index'))

        dests = request.headers['destinations'].split(",")
        probs = request.headers['probs'].split(",")  # str > string list

        destinations = url.destinations.all()

        url.destinations.clear()
        for i in range(len(dests)):
            destination, probability = dests[i], probs[i]
            if sum([destination == x.url for x in destinations]) > 0:
                dest = Destination.objects.filter(url=destination).first()  # gets the object with that destination
                dest.prob = float(probability)
                dest.save()

                url.destinations.add(dest)
            else:
                dest = Destination.objects.create(views=0, url=destination, prob=probability)
                dest.save()

                url.destinations.add(dest)

        url.title = request.headers['title']

        url.save()

        print("Updated: ", url.link_string)

        return HttpResponseRedirect(reverse_lazy('account-view'))

    @staticmethod
    def get_url(link_string):
        return URL.objects.filter(link_string=link_string).first()


# MISC Stuff
class TOS(TemplateView):
    template_name = 'misc/tos.html'


class PrivacyPolicy(TemplateView):
    template_name = 'misc/privacy.html'


class Robots(TemplateView):
    template_name = "robots.txt"


def get_dest(request, link_string):
    """
    Redirects the user to a random page.
    """
    dest = get_object_or_404(URL, link_string=link_string)
    print("Got dest")
    url = urlparse(dest.get_destination())
    if not url.scheme:
        url = url._replace(scheme="http")

    return HttpResponseRedirect(url.geturl())


def get_dest_info(request, link_string):
    """Provides information about a destination. View count if the user is logged in."""
    url = get_object_or_404(URL, link_string=link_string)
    return render(request, "urls/info.html", {'url': url})
