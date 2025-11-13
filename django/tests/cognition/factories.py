import factory
from factory.django import DjangoModelFactory
from cognition.models import CognitionFrame
from ..common.factories import LogFactory


class CognitionFrameFactory(DjangoModelFactory):
    class Meta:
        model = CognitionFrame

    log = factory.SubFactory(LogFactory)
    frame_number = factory.Sequence(lambda n: n + 1)
    frame_time = factory.Sequence(lambda n: n + 30)
