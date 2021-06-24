from django.contrib import admin
from dfirtrack_artifacts.models import Artifact, Artifactpriority, Artifactstatus, Artifacttype
# Register your models here.
admin.site.register(Artifact)
admin.site.register(Artifactpriority)
admin.site.register(Artifactstatus)
admin.site.register(Artifacttype)
