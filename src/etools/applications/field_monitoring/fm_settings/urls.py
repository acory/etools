from django.conf.urls import include, url

from rest_framework_nested import routers

from etools.applications.field_monitoring.data_collection.routers import NestedBulkRouter
from etools.applications.field_monitoring.fm_settings import views

root_api = routers.SimpleRouter()
root_api.register(r'methods', views.MethodsViewSet, basename='methods')
root_api.register(r'attachments', views.FieldMonitoringGeneralAttachmentsViewSet, basename='general-attachments')
root_api.register(r'log-issues', views.LogIssuesViewSet, basename='log-issues')
root_api.register(r'sites', views.LocationSitesViewSet, basename='sites')
root_api.register(r'locations', views.FMLocationsViewSet, basename='locations')
root_api.register(r'categories', views.CategoriesViewSet, basename='categories')
root_api.register(r'questions', views.QuestionsViewSet, basename='questions')

log_issues_api = NestedBulkRouter(root_api, r'log-issues')
log_issues_api.register(r'attachments', views.LogIssueAttachmentsViewSet, basename='log-issue-attachments')

app_name = 'field_monitoring_settings'
urlpatterns = [
    url(r'^interventions/(?P<intervention_pk>[0-9]+)/locations/', views.InterventionLocationsView.as_view(),
        name='intervention-locations'),
    url(r'^results/', views.ResultsView.as_view(), name='results-list'),
    url(r'^locations/country/', views.LocationsCountryView.as_view(), name='locations-country'),
    url(r'^', include(log_issues_api.urls)),
    url(r'^', include(root_api.urls)),
]
