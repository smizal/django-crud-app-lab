from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    
    # # CBV's path for Event model 
    path('events/', views.EventList.as_view(), name='event-index'),
    path('events/<int:event_id>', views.event_detail, name='event-detail'),
    # path('events/<int:pk>', views.EventDetail.as_view(), name='event-detail'),
    path('events/<int:pk>/update/', views.EventUpdate.as_view(), name='event-update'),
    path('events/<int:pk>/delete/', views.EventDelete.as_view(), name='event-delete'),
    path('events/create/', views.EventCreate.as_view(), name='event-create'),
    
    path('features/', views.FeatureList.as_view(), name='feature-index'),
    path('features/<int:pk>', views.FeatureDetail.as_view(), name='feature-detail'),
    path('features/<int:pk>/update/', views.FeatureUpdate.as_view(), name='feature-update'),
    path('features/<int:pk>/delete/', views.FeatureDelete.as_view(), name='feature-delete'),
    path('features/create/', views.FeatureCreate.as_view(), name='feature-create'),

    path('events/<int:event_id>/add-room/', views.add_room, name='add-room'),

    path('events/<int:event_id>/associate-feature/<int:feature_id>/', views.associate_feature, name='associate-feature'),
    path('events/<int:event_id>/remove-feature/<int:feature_id>/', views.remove_feature, name='remove-feature'),
    path('accounts/signup/', views.signup, name='signup'),
]
