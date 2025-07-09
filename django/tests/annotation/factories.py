import factory
from factory.django import DjangoModelFactory
from ..image.factories import NaoImageFactory
from annotation.models import Annotation
import random

class AnnotationFactory(DjangoModelFactory):
    class Meta:
        model = Annotation

    image = factory.SubFactory(NaoImageFactory)
    type = factory.Iterator([choice[0] for choice in Annotation.Types.choices])
    class_name = factory.Iterator([choice[0] for choice in Annotation.Classes.choices])
    concealed = factory.Faker("boolean")
    is_empty = factory.Faker("boolean")
    validated = factory.Faker("boolean")
    data = factory.LazyAttribute(
        lambda _: {
            "x": random.uniform(0, 0.83),
            "y": random.uniform(0, 0.88),
            "width": random.uniform(0, 1),
            "height": random.uniform(0, 1),
        }
    )
    
