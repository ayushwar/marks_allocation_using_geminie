from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentAnswerViewSet, analyze_student_answers
from . import views
from .views import results_page
router = DefaultRouter()
router.register(r'answer', StudentAnswerViewSet)


urlpatterns = [
    # path('answer/results/', analyze_student_answers),
    path('', views.student_login, name='student_login'),
    path('answer/<str:roll_no>/', views.answer_page, name='answer_page'),
    path('results/', views.results_page, name='results_page'), 
    path('aice/results/', results_page, name='results_page'), 
    path('', include(router.urls)),

]

# urlpatterns += [
#     path('debug/urls/', show_all_urls),
# ]
