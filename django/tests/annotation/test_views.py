import pytest
import json
from .factories import AnnotationFactory
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
        ann2 = AnnotationFactory.create()
        response = auth_client.get('/api/annotations/')
        assert response.status_code == 200
        assert len(json.loads(response.content)) >= 2
        # Filter by image
        response = auth_client.get('/api/annotations/', {'image': ann1.image.id})
        assert response.status_code == 200
        assert all(a['image'] == ann1.image.id for a in json.loads(response.content))

    def test_annotation_viewset_create_and_duplicate(self, admin_client):
        ann = AnnotationFactory.build()
        data = {
            'image': ann.image.id,
            'type': ann.type,
            'class_name': ann.class_name,
            'concealed': ann.concealed,
            'data': ann.data,
        }
        response = admin_client.post('/api/annotations/', data, format='json')
        assert response.status_code == 201
        # Try to create duplicate
        response2 = admin_client.post('/api/annotations/', data, format='json')
        assert response2.status_code == 200
        assert response2.json()['id'] == response.json()['id']

    def test_annotation_task_basic(self, auth_client):
        ann = AnnotationFactory.create(validated=False)
        response = auth_client.get('/api/annotation-task/')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert 'result' in data
        assert any(str(ann.image.frame.log.id) in link for link in data['result'])

    def test_annotation_task_prio_only(self, auth_client):
        response = auth_client.get('/api/annotation-task/', {'prio_only': 'true'})
        assert response.status_code == 200
        assert json.loads(response.content)['result'] == []
