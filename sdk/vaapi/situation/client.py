import typing
from json.decoder import JSONDecodeError

from ..core.api_error import ApiError
from ..core.client_wrapper import SyncClientWrapper
from ..core.jsonable_encoder import jsonable_encoder
from ..core.pydantic_utilities import pydantic_v1
from ..core.request_options import RequestOptions
from ..types.situation import Situation

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class SituationClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def get(
        self, id: int, *, request_options: typing.Optional[RequestOptions] = None
    ) -> Situation:
        """
        Retrieve a specific situation by its ID.

        Parameters
        ----------
        id : int
            A unique integer value identifying the situation.
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        Situation
            The requested situation object.

        Examples
        --------
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )
        situation = client.situation.get(id=1)
        """
        _response = self._client_wrapper.httpx_client.request(
            f"api/situations/{jsonable_encoder(id)}/",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(Situation, _response.json())  # type: ignore
            _response_json = _response.json()

        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete(
        self, id: int, *, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Deletes a Situation.

        <Warning>This action can't be undone!</Warning>

        You will need to supply the situation's unique ID. You can find the ID in
        the django admin panel or in the situation settings in the UI.

        Parameters
        ----------
        id : int
            A unique integer value identifying this situation.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )
        client.situation.delete(
            id=1,
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"api/situations/{jsonable_encoder(id)}/",
            method="DELETE",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def update(
        self,
        id: int,
        *,
        game: typing.Optional[int] = OMIT,
        log: typing.Optional[int] = OMIT,
        GameControllerMessage: typing.Optional[typing.Dict[str, typing.Any]]= OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> Situation:
        """
        Update a specific situation by its ID.

        Parameters
        ----------
        id : int
            A unique integer value identifying the situation to update.
        game : typing.Optional[int]
            Foreign key to the game this situation is from.
        log : typing.Optional[int]
            Foreign key to the log this situation is from.
        GameControllerMessage : typing.Optional[typing.Dict[str, typing.Any]]
            Message from GameController in JSON Format
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        Situation
            The updated situation object.

        Examples
        --------
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )
        updated_situation = client.situation.update(
            id=1,
            log=200
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"api/situations/{jsonable_encoder(id)}/",
            method="PATCH",
            json={
                "game": game,
                "log": log,
                "GameControllerMessage": GameControllerMessage,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(Situation, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def list(
        self,
        request_options: typing.Optional[RequestOptions] = None,
        **filters: typing.Any,
    ) -> typing.List[Situation]:
        """
        List all situations

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.
        **filters : typing.Any
            Optional query parameters
            
        Returns
        -------
        typing.List[Situation]
            A list of situation objects.

        Examples
        --------
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )
        
        # List all situations
        all_situations = client.situation.list()
        
        # List situations with specific filters
        filtered_situations = client.situation.list(game=1)
        """
        query_params = {k: v for k, v in filters.items() if v is not None}
        _response = self._client_wrapper.httpx_client.request(
            "api/situations/",
            method="GET",
            request_options=request_options,
            params=query_params,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(
                    typing.List[Situation], _response.json()
                )  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create(
        self,
        *,
        game: typing.Optional[int] = OMIT,
        log: typing.Optional[int] = OMIT,
        GameControllerMessage: typing.Optional[typing.Dict[str, typing.Any]]= OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> Situation:
        """
        Create a new situation.

        Parameters
        ----------
        game : typing.Optional[int]
            Foreign key to the game this situation is from.
        log : typing.Optional[int]
            Foreign key to the log this situation is from.
        GameControllerMessage : typing.Optional[typing.Dict[str, typing.Any]]
            Message from GameController in JSON Format
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        Situation
            The created situation object.

        Examples
        --------
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )
        new_situation = client.situation.create(
            game=1,
            GameControllerMessage=JSONMessage
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "api/situations/",
            method="POST",
            json={
                "game": game,
                "log": log,
                "GameControllerMessage": GameControllerMessage,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(Situation, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    