from django.shortcuts import render, redirect
from .models import Event, Feature, Room
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RoomForm
from django.contrib.auth.views import LoginView

# Create your views here.
# Events classes
class Home(LoginView):
    template_name = 'home.html'

class EventList(LoginRequiredMixin, ListView):
    model = Event

# class EventDetail(LoginRequiredMixin, DetailView):
#     features = Feature.objects.all()
#     # event = Event.objects.all()
#     # toys_cat_doesnt_have = Feature.objects.exclude(id__in = event.features.all().values_list('id'))
#     room_form = RoomForm()
#     model = Event

@login_required
def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    features = Feature.objects.all()
    features_event_doesnt_have = Feature.objects.exclude(id__in = event.features.all().values_list('id'))
    room_form = RoomForm()
    return render(request, 'my_app/event_detail.html', {'event': event, 'room_form': room_form, 'features': features_event_doesnt_have})

class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['title', 'description', 'date']

class EventDelete(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = '/events/'

class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['title', 'description', 'date']

    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the cat
        # Let the CreateView do its job as usual
        return super().form_valid(form)

# Features classes
class FeatureList(LoginRequiredMixin, ListView):
    model = Feature

class FeatureDetail(LoginRequiredMixin, DetailView):
    model = Feature

class FeatureUpdate(LoginRequiredMixin, UpdateView):
    model = Feature
    fields = ['title', 'description', 'color']

class FeatureDelete(LoginRequiredMixin, DeleteView):
    model = Feature
    success_url = '/features/'

class FeatureCreate(LoginRequiredMixin, CreateView):
    model = Feature
    fields = ['title', 'description', 'color']

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('event-index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
    # Same as: 
    # return render(
    #     request, 
    #     'signup.html',
    #     {'form': form, 'error_message': error_message}
    # )

@login_required
def add_room(request, event_id):
    form = RoomForm(request.POST)
    if form.is_valid():
        new_room = form.save(commit=False)
        new_room.event_id = event_id
        new_room.save()
    return redirect('event-detail', event_id=event_id)

@login_required
def associate_feature(request, event_id, feature_id):
    Event.objects.get(id=event_id).features.add(feature_id)
    return redirect('event-detail', event_id=event_id)

@login_required
def remove_feature(request, event_id, feature_id):
    event = Event.objects.get(id=event_id)
    feature = Feature.objects.get(id=feature_id)
    event.features.remove(feature)
    return redirect('event-detail', event_id=event.id)