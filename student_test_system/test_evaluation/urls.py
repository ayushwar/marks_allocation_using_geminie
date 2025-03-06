from django.urls import path, include  # Make sure to import 'include'
from rest_framework.routers import DefaultRouter
from .views import StudentAnswerViewSet, evaluate_answer, student_results
from django.http import JsonResponse

router = DefaultRouter()
router.register(r'answers', StudentAnswerViewSet)
def home(request):
    return JsonResponse({
        "message": "Welcome to the Student Test System API!",
        "endpoints": [
            "/admin/",
            "/api/",
            "/api/evaluate/<roll_no>/",
            "/results/<roll_no>/"
        ]
    })

# urlpatterns = [
#     path('', home, name="home"),  # ✅ This handles the root URL
#     path('evaluate/<str:roll_no>/', evaluate_answer, name='evaluate-answer'),
# ]

urlpatterns = [
    path('', home, name="home"),  # ✅ This handles the root URL
    path('evaluate/<str:roll_no>/', evaluate_answer, name='evaluate-answer'),
    path('api/', include(router.urls)),
    path('api/evaluate/<str:roll_no>/', evaluate_answer, name='evaluate-answer'),
    path('results/', student_results, name='student-results'),
     path('submit-answer/', evaluate_answer, name='submit-answer'),
]