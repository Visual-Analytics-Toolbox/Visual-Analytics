from common.models import Log
from typing import Self

class VideoFilter:
    def __init__(self, queryset, query_params) -> None:
        self.qs = queryset
        self._params = query_params

    def filter_game(self) -> Self:
        if "game" in self._params:
            game_id = int(self._params["game"])
            self.qs = self.qs.filter(game=game_id)
        return self

    def filter_log(self) -> Self:
        if "log" in self._params:
            log_id = int(self._params["log"])
            # TODO: get game_id here
            game_id=Log.objects.get(id=log_id).game
            self.qs = self.qs.filter(game=game_id)
        return self

    def filter_experiment(self) -> Self:
        if "experiment" in self._params:
            experiment_id = int(self._params["experiment"])
            self.qs = self.qs.filter(experiment=experiment_id)
        return self

    def filter_type(self) -> Self:
        if "type" in self._params:
            video_type = self._params["type"]
            self.qs = self.qs.filter(type=video_type)
        return self


class RobotFilter:
    def __init__(self, queryset, query_params) -> None:
        self.qs = queryset
        self._params = query_params

    def filter_head_number(self) -> Self:
        if "head_number" in self._params:
            head_number = int(self._params["head_number"])
            self.qs = self.qs.filter(head_number=head_number)
        return self

    def filter_body_serial(self) -> Self:
        if "body_serial" in self._params:
            body_serial = self._params["body_serial"]
            self.qs = self.qs.filter(body_serial=body_serial)
        return self