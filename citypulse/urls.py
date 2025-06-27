from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import report_issue, user_profile, CivicIssueListView, UserIssuesListView, RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('report/', report_issue, name='report-issue'),
    path('profile/', user_profile, name='user_profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('issues/', CivicIssueListView.as_view(), name='issue-list'),
    path('my-issues/', UserIssuesListView.as_view(), name='user-issue-list'),
    ]
