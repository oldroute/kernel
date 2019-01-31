from django.urls import path, include
from .views import *


urlpatterns = [
    path('root/', BookRootView.as_view()),
    path('page/<int:pk>/', PageDetailView.as_view()),
    path('page/<int:parent_id>/children/', PageChildrenListView.as_view()),
    path('page/<int:page>/tasks/', TaskListView.as_view()),
    path('task/<int:pk>/', TaskDetailView.as_view()),

]