from typing import Self


class AnnotationFilter:
    def __init__(self, queryset, query_params) -> None:
        self.qs = queryset
        self._params = query_params

    def filter_image(self) -> Self:
        if "image" in self._params:
            image_id = int(self._params["image"])
            self.qs = self.qs.filter(image=image_id)
        return self

    def filter_log(self) -> Self:
        if "log" in self._params:
            log_id = int(self._params["log"])
            self.qs = self.qs.filter(image__frame__log=log_id)
        return self

    def filter_camera(self) -> Self:
        if "camera" in self._params:
            camera = self._params["camera"]
            self.qs = self.qs.filter(image__camera=camera)
        return self

    def filter_validated(self) -> Self:
        if "validated" in self._params:
            validated = self._params["validated"]
            # Convert validated to boolean if it's a string
            if isinstance(validated, str):
                validated = validated.lower() == "true"
            self.qs = self.qs.filter(validated=validated)
        return self

    def filter_type(self) -> Self:
        pass
    
    def filter_class(self) -> Self:
        pass
    
    def filter_empty(self) -> Self:
        pass
    
    def filter_concealed(self) -> Self:
        if "concealed" in self._params:
            concealed = self._params["concealed"]
            # Convert concealed to boolean if it's a string
            if isinstance(concealed, str):
                concealed = concealed.lower() == "true"
            self.qs = self.qs.filter(concealed=concealed)
        return self
    
