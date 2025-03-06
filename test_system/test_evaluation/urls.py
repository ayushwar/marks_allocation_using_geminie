from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentAnswerViewSet, analyze_student_answers
router = DefaultRouter()
router.register(r'answer', StudentAnswerViewSet)


urlpatterns = [
    path('answer/results/', analyze_student_answers),
    path('', include(router.urls)),
]

# urlpatterns += [
#     path('debug/urls/', show_all_urls),
# ]
