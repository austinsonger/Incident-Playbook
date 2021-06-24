from django.urls import path
from dfirtrack_artifacts.exporter.spreadsheet import xls
from dfirtrack_artifacts.views import artifact_view, artifactpriority_view, artifactstatus_view, artifacttype_view

urlpatterns = (
    # urls for Artifact
    path(r'artifact/', artifact_view.ArtifactListView.as_view(), name='artifacts_artifact_list'),
    path(r'artifact/closed/', artifact_view.ArtifactClosedView.as_view(), name='artifacts_artifact_closed'),
    path(r'artifact/all/', artifact_view.ArtifactAllView.as_view(), name='artifacts_artifact_all'),
    path(r'artifact/create/', artifact_view.ArtifactCreateView.as_view(), name='artifacts_artifact_create'),
    path(r'artifact/detail/<int:pk>/', artifact_view.ArtifactDetailView.as_view(), name='artifacts_artifact_detail'),
    path(r'artifact/update/<int:pk>/', artifact_view.ArtifactUpdateView.as_view(), name='artifacts_artifact_update'),
    path(r'artifact/exporter/spreadsheet/xls/artifact/', xls.artifact, name='artifact_exporter_spreadsheet_xls'),
)

urlpatterns += (
    # urls for Artifactpriority
    path(r'artifactpriority/', artifactpriority_view.ArtifactpriorityListView.as_view(), name='artifacts_artifactpriority_list'),
    path(r'artifactpriority/detail/<int:pk>/', artifactpriority_view.ArtifactpriorityDetailView.as_view(), name='artifacts_artifactpriority_detail'),
)

urlpatterns += (
    # urls for Artifactstatus
    path(r'artifactstatus/', artifactstatus_view.ArtifactstatusListView.as_view(), name='artifacts_artifactstatus_list'),
    path(r'artifactstatus/detail/<int:pk>/', artifactstatus_view.ArtifactstatusDetailView.as_view(), name='artifacts_artifactstatus_detail'),
)

urlpatterns += (
    # urls for Artifacttype
    path(r'artifacttype/', artifacttype_view.ArtifacttypeListView.as_view(), name='artifacts_artifacttype_list'),
    path(r'artifacttype/create/', artifacttype_view.ArtifacttypeCreateView.as_view(), name='artifacts_artifacttype_create'),
    path(r'artifacttype/detail/<int:pk>/', artifacttype_view.ArtifacttypeDetailView.as_view(), name='artifacts_artifacttype_detail'),
    path(r'artifacttype/update/<int:pk>/', artifacttype_view.ArtifacttypeUpdateView.as_view(), name='artifacts_artifacttype_update'),
)
