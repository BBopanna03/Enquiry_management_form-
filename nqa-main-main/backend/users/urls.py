from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView, CreateUserView, EnquiryListView, EnquiryDetailView,
    StudentEnquiryListCreate, StudentEnquiryDetailView,
    DemoListListCreate, DemoListDetailView,
    CourseListView, BatchTimingListView,
    AdminOnlyView, CounsellorOnlyView, AccountsOnlyView, HROnlyView, SampleView , HRListAPIView,create_student_placement
)
from .views import student_placement_view
urlpatterns = [
    path('', SampleView.as_view(), name='api-root'),  # root returns accessible message
    path('login/', LoginView.as_view(), name='login'),
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('enquiries/', EnquiryListView.as_view(), name='enquiry-list'),
    path('enquiries/<int:pk>/', EnquiryDetailView.as_view(), name='enquiry-detail'),
    path('student_enquiries/', StudentEnquiryListCreate.as_view(), name='student-enquiry-list-create'),
    path('student_enquiries/<int:pk>/', StudentEnquiryDetailView.as_view(), name='student-enquiry-detail'),
    path('demo_lists/', DemoListListCreate.as_view(), name='demo-list-list-create'),
    path('demo_lists/<int:pk>/', DemoListDetailView.as_view(), name='demo-list-detail'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('batch_timings/', BatchTimingListView.as_view(), name='batch-timing-list'),
    # Role-based views for testing
    path('admin-only/', AdminOnlyView.as_view(), name='admin-only'),
    path('counsellor-only/', CounsellorOnlyView.as_view(), name='counsellor-only'),
    path('accounts-only/', AccountsOnlyView.as_view(), name='accounts-only'),
    path('hr-only/', HROnlyView.as_view(), name='hr-only'),
    path('api/hr-list/', HRListAPIView.as_view(), name='hr-list'),
    path("student-placement/", student_placement_view, name="student-placement"),
    path("create-student-placement/", create_student_placement, name="create-student-placement"),
]