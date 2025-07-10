import pytest
from annotation.models import Annotation
from .factories import AnnotationFactory


pytestmark = pytest.mark.django_db

class TestAnnotationModel:
    def test_create_annotation_minimal(self):
        AnnotationFactory.create()
        assert Annotation.objects.count() == 1
        db_ann = Annotation.objects.first()
        assert isinstance(db_ann, Annotation)
        assert db_ann.image is not None
        assert db_ann.type in dict(Annotation.Types.choices)
        assert db_ann.class_name in dict(Annotation.Classes.choices)
        assert isinstance(db_ann.concealed, bool)
        assert isinstance(db_ann.validated, bool)
        assert isinstance(db_ann.data, dict)
        assert db_ann.created is not None
        assert db_ann.modified is not None

    def test_type_and_class_choices(self):
        for t, _ in Annotation.Types.choices:
            ann = AnnotationFactory.create(type=t)
            assert ann.type == t
        for c, _ in Annotation.Classes.choices:
            ann = AnnotationFactory.create(class_name=c)
            assert ann.class_name == c

    def test_get_color(self):
        for c, _ in Annotation.Classes.choices:
            color = Annotation.Classes.get_color(c)
            assert color is None or isinstance(color, str)
            if color:
                assert color.startswith("#")

    def test_foreign_key_cascade(self):
        annotation = AnnotationFactory.create()
        image = annotation.image
        image.delete()
        assert Annotation.objects.count() == 0

