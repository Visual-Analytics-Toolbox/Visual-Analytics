from typing import Self

class SituationFilter:
    def __init__(self, queryset, query_params) -> None:
        self.qs = queryset
        self._params = query_params

    def filter_log(self) -> Self:
        if "log" in self._params:
            log_id = int(self._params["log"])
            self.qs = self.qs.filter(log=log_id)
        return self

    def filter_game(self) -> Self:
        if "game" in self._params:
            game_id = int(self._params["game"])
            self.qs = self.qs.filter(game=game_id)
        return self
