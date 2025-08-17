from typing import Self

class ImageFilter:
    def __init__(self, queryset, query_params) -> None:
        self.qs = queryset
        self._params = query_params

    def filter_camera(self) -> Self:
        if "camera" in self._params:
            camera = self._params["camera"]
            self.qs = self.qs.filter(camera=camera)
        return self
    
    def filter_imagetype(self) -> Self:
        pass
    
    def filter_log(self) -> Self:
        if "log" in self._params:
            log_id = int(self._params["log"])
            self.qs = self.qs.filter(frame__log=log_id)
        return self

    def filter_framenumber(self) -> Self:
        if "frame_number" in self._params:
            frame_number = int(self._params["frame_number"])
            self.qs = self.qs.filter(frame__frame_number=frame_number)
        return self
    
    def filter_image_tag(self) -> Self:
        pass

    """
    filter on annotation related values
    """
    #FIXME using annotation and validated together gives weird results
    # together gives more results then using just validated
    def filter_annotation(self) -> Self:
        if "annotation" in self._params:
            annotation_exist = self._params["annotation"]
            # Convert annotation to boolean if it's a string
            if isinstance(annotation_exist, str):
                annotation_exist = annotation_exist.lower() == "true"
                print(annotation_exist)
                self.qs = self.qs.filter(annotation__isnull= not annotation_exist)
        return self

    def filter_validated(self) -> Self:
        """
        Note that setting validated to either true or false will only return images that have annotations
        Note: If you have an image with validated and unvalidated annotations it will be included no matter what you set for the validated flag
        """
        if "validated" in self._params:
            validated = self._params["validated"]
            # Convert validated to boolean if it's a string
            if isinstance(validated, str):
                validated = validated.lower() == "true"
                self.qs = self.qs.filter(annotation__validated=validated)
        return self
    
    def filter_annotation_type(self) -> Self:
        pass
    
    def filter_annotation_class(self) -> Self:
        pass
    
    def filter_annotation_tags(self) -> Self:
        pass
