from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q, F
from .models import Annotation
from .serializers import AnnotationSerializer
from .annotation_filter import AnnotationFilter


def generic_filter(queryset, query_params):
    filters = Q()
    for field in Annotation._meta.fields:
        param_value = query_params.get(field.name)
        if param_value == "None" or param_value == "null":
            filters &= Q(**{f"{field.name}__isnull": True})
        elif param_value:
            filters &= Q(**{field.name: param_value})
    # apply filters if provided
    return queryset.filter(filters)


class AnnotationCount(APIView):
    def get(self, request):
        # Get filter parameters from query string
        query_params = request.query_params.copy()

        if "log" in query_params.keys():
            log_id = int(query_params.pop("log")[0])
            qs = Annotation.objects.filter(image__frame__log=log_id)
        else:
            qs = Annotation.objects.all()

        # Handle boolean flags here
        if "validated" in query_params.keys():
            validated_value = query_params.pop("validated")[0]
            if validated_value == "true":
                qs = qs.filter(validated=True)
            elif validated_value == "false":
                qs = qs.filter(validated=False)
        # TODO we have other boolean flags and maybe there is way to do that better

        filters = Q()
        for field in Annotation._meta.fields:
            param_value = query_params.get(field.name)
            if param_value == "None" or param_value == "null":
                filters &= Q(**{f"{field.name}__isnull": True})
                # print(f"filter with {field.name} = {param_value}")
            elif param_value:
                # print(f"filter with {field.name} = {param_value}")
                filters &= Q(**{field.name: param_value})

        # apply filters if provided
        qs = qs.filter(filters)

        # get the count
        count = qs.count()

        return Response({"count": count}, status=status.HTTP_200_OK)


class AnnotationViewSet(viewsets.ModelViewSet):
    """
    This endpoint can be used to get existing annotations together with the image url under constraints for example
    for creating datasets for ML

    This endpoint is not suitable for use in the validation UI since its missing the image tag information

    TODO: add pagination for this
    TODO: check if we can actually use this easily to create datasets since it return multiple annotations per image seperately
    this might be annoying for some annotation formats
    """

    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer

    def get_queryset(self):
        qs = Annotation.objects.all()
        # filter all possible arguments here via the builder pattern
        filter = AnnotationFilter(qs, self.request.query_params)
        qs = filter.filter_image().filter_log().filter_camera().filter_validated().qs

        # annotate with frame number and image url
        qs = qs.annotate(frame_number=F("image__frame__frame_number"))
        qs = qs.annotate(image_url=F("image__image_url"))

        return qs

    def create(self, request, *args, **kwargs):
        # TODO write a create function that checks if json is exactly the same and if so ignores the insert
        # Get the data from the request
        image_id = request.data.get("image")
        annotation_type = request.data.get("type")
        class_name = request.data.get("class_name")
        concealed = request.data.get("concealed", False)
        data = request.data.get("data")

        # Check if all required fields are present
        if not all([image_id, annotation_type, class_name, data]):
            return Response(
                {"detail": "Missing required fields"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Convert concealed to boolean if it's a string
        if isinstance(concealed, str):
            concealed = concealed.lower() == "true"

        # TODO when we use a new yolo model we will get slightly different results, we need to catch this here
        # Look for existing annotation with the same fields
        existing_annotation = Annotation.objects.filter(
            image_id=image_id,
            type=annotation_type,
            class_name=class_name,
            concealed=concealed,
            data=data,  # JSONField comparison will handle the structure
        ).first()

        if existing_annotation:
            # Return the existing annotation
            serializer = self.get_serializer(existing_annotation)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # No existing annotation found, proceed with normal creation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
