import pytest
import json
import factory
from .factories import AnnotationFactory
from ..image.factories import NaoImageFactory
from annotation.models import Annotation

pytestmark = pytest.mark.django_db

class TestAnnotationViews:
    def test_annotation_count_basic(self, auth_client):
        AnnotationFactory.create_batch(3, validated=False)
        response = auth_client.get('/api/annotation-count/')
        assert response.status_code == 200
        assert json.loads(response.content)["count"] == 3

    def test_annotation_count_validated_filter(self, auth_client):
        AnnotationFactory.create_batch(2, validated=True)
        AnnotationFactory.create_batch(1, validated=False)
        response = auth_client.get('/api/annotation-count/', {'validated': 'true'})
        assert response.status_code == 200
        assert json.loads(response.content)["count"] == 2
        response = auth_client.get('/api/annotation-count/', {'validated': 'false'})
        assert json.loads(response.content)["count"] == 1

    def test_annotation_viewset_list_and_filter(self, auth_client):
        ann1 = AnnotationFactory.create()
        AnnotationFactory.create()
        response = auth_client.get('/api/annotations/')
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 2
        # Filter by image
        response = auth_client.get('/api/annotations/', {'image': ann1.image.id})
        assert response.status_code == 200
        assert all(a['image'] == ann1.image.id for a in json.loads(response.content))
   
    def test_annotation_viewset_create_and_duplicate(self, admin_client):
         # we need to do create to insert related data into db otherwise post is not working for this annotation
        img = NaoImageFactory.create()
        # we can create JSON Objects directly with factory boy
        ann = factory.build(dict,FACTORY_CLASS=AnnotationFactory,image=img.id)
        response = admin_client.post('/api/annotations/', ann, format='json')
        assert response.status_code == 201
        # Try to create duplicate
        response2 = admin_client.post('/api/annotations/', ann, format='json')
        assert response2.status_code == 200
        assert response2.json()['id'] == response.json()['id']    

    def test_validate(self,admin_client):
        ann = AnnotationFactory.create(validated=False)
        data = {'validated':'true'}
        response = admin_client.patch(f'/api/annotations/{ann.id}/',data,format='json')
        assert response.status_code == 200
        assert Annotation.objects.get(id=ann.id).validated

    def test_move(self,admin_client):
        ann = AnnotationFactory.create(validated=False)
        data = {'data':factory.build(dict,FACTORY_CLASS=AnnotationFactory).get('data')}
        print(data)
        response = admin_client.patch(f'/api/annotations/{ann.id}/',data,format='json')
        assert response.status_code == 200
        assert Annotation.objects.get(id=ann.id).data == data.get('data')

    def test_delete(self,admin_client):
        ann = AnnotationFactory.create()
        response = admin_client.delete(f'/api/annotations/{ann.id}/')
        assert response.status_code == 204
        assert Annotation.objects.filter(id=ann.id).count() == 0
    