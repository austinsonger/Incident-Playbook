from dfirtrack_api.serializers.dfirtrack_artifacts import ArtifactSerializer, ArtifactstatusSerializer, ArtifacttypeSerializer
from dfirtrack_artifacts.models import Artifact, Artifactstatus, Artifacttype
from rest_framework import generics

class ArtifactListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = Artifact.objects.all()
    serializer_class = ArtifactSerializer

class ArtifactDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = Artifact.objects.all()
    serializer_class = ArtifactSerializer

class ArtifactstatusListApi(generics.ListAPIView):
    """ all objects, allowed: GET """

    queryset = Artifactstatus.objects.all()
    serializer_class = ArtifactstatusSerializer

class ArtifactstatusDetailApi(generics.RetrieveAPIView):
    """ single object, allowed: GET """

    queryset = Artifactstatus.objects.all()
    serializer_class = ArtifactstatusSerializer

class ArtifacttypeListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = Artifacttype.objects.all()
    serializer_class = ArtifacttypeSerializer

class ArtifacttypeDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = Artifacttype.objects.all()
    serializer_class = ArtifacttypeSerializer
