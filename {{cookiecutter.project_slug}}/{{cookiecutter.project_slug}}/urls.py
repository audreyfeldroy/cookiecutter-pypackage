from django.urls import path

from netbox.views.generic import ObjectChangeLogView
from . import models, views


urlpatterns = (

    # Access lists
    path('access-lists/', views.AccessListListView.as_view(), name='accesslist_list'),
    path('access-lists/add/', views.AccessListEditView.as_view(), name='accesslist_add'),
    path('access-lists/<int:pk>/', views.AccessListView.as_view(), name='accesslist'),
    path('access-lists/<int:pk>/edit/', views.AccessListEditView.as_view(), name='accesslist_edit'),
    path('access-lists/<int:pk>/delete/', views.AccessListDeleteView.as_view(), name='accesslist_delete'),
    path('access-lists/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='accesslist_changelog', kwargs={
        'model': models.AccessList
    }),

    # Access list rules
    path('rules/', views.AccessListRuleListView.as_view(), name='accesslistrule_list'),
    path('rules/add/', views.AccessListRuleEditView.as_view(), name='accesslistrule_add'),
    path('rules/<int:pk>/', views.AccessListRuleView.as_view(), name='accesslistrule'),
    path('rules/<int:pk>/edit/', views.AccessListRuleEditView.as_view(), name='accesslistrule_edit'),
    path('rules/<int:pk>/delete/', views.AccessListRuleDeleteView.as_view(), name='accesslistrule_delete'),
    path('rules/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='accesslistrule_changelog', kwargs={
        'model': models.AccessListRule
    }),

)
