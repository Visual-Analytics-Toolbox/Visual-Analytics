import factory
from factory.django import DjangoModelFactory
from ..cognition.factories import CognitionFrameFactory
from image.models import NaoImage


class NaoImageFactory(DjangoModelFactory):
    class Meta:
        model = NaoImage

    frame = factory.SubFactory(CognitionFrameFactory)
    camera = factory.Iterator([choice[0] for choice in NaoImage.Camera.choices])
    type = factory.Iterator([choice[0] for choice in NaoImage.Type.choices])
    image_url = factory.Faker("file_path")
    blurredness_value = factory.Faker("random_int", min=0, max=100)
    brightness_value = factory.Faker("random_int", min=0, max=100)
    resolution = factory.Faker("bothify", text="####x####x#")