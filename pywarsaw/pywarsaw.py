import os
from typing import Union

from .client import Client
from .exceptions import WrongQueryParameters, UnauthorizedAccess, WrongAPIKey
from .objects import (
    Shrub,
    ShrubsGroup,
    Tree,
    TreesGroup,
    Forest,
    MunincipalWaste,
    AirQuality,
    Ijp,
    AirData,
    AirStationAddress,
    Defibrillator,
    DefibrillatorGeometry,
    DefibrillatorProperties,
    VehicleLocation,
    StopSet,
    StopLine,
    LineTimetable,
    CycleTrack,
    CycleStation,
    ParkingLot,
    SubwayEntrance,
    StopInfo,
    Theater,
    InternetAccess,
    ComputerPurpose,
)


class Mermaid(Client):
    """A client for interacting with Warsaw Open Data API.

    Args:
        headers (dict): The headers to include in the request made to the API.
            Defaults to {"User-Agent": "pywarsaw}
        api_key (str): The API key to use for authentication.
            Defaults to None.
    """

    def __init__(
        self,
        headers: dict = {"User-Agent": "pywarsaw"},
        api_key: str = None,
    ):
        super().__init__()
        self.headers = headers
        self.api_key = api_key

    @staticmethod
    def _build_url(endpoint, **kwargs) -> str:
        """Builds a url for a specified endpoint using provided parameters.

        Args:
           endpoint (str): The endpoint for the API call.
            **kwargs: Additional parameters to include in the url.

        Returns:
            str: The built url.
        """
        base_url = "https://api.um.warszawa.pl/api/action/"

        url = (
            base_url
            + endpoint
            + "?"
            + "&".join(
                f"{key}={item}" for key, item in kwargs.items() if item is not None
            )
        )
        return url

    async def _get_data(self, url: str) -> dict:
        """Retrieves data from a specified url using an asynchronous HTTP GET request.

        Args:
            url (str): The url to retrieve data from.

        Returns:
            dict: The data retrieved from the url.

        Raises:
            HTTPError: If the GET request returns an HTTP error status code.
            WrongQueryParameters: If the query parameters are wrong.
            WrongAPIKey: If the provided API key is wrong.
            UnauthorizedAccess: If API key is not provided.
        """

        res = await super()._get(url)

        # handle exceptions
        if res["result"] in (
            "Błędna metoda lub parametry wywołania",
            "Wfs error: IllegalArgumentException: FeatureMember list is empty",
        ):
            await super().close()
            raise WrongQueryParameters()

        if res["result"] == "false" and res["error"] == "Błędny apikey lub jego brak":
            await super().close()
            raise WrongAPIKey()
        if (
            res["result"] == "false"
            and res["error"] == "Nieautoryzowany dostęp do danych"
        ):
            await super().close()
            raise UnauthorizedAccess()

        return res

    async def get_shrubs(
        self,
        limit: Union[int, str, None] = None,
        q: Union[str, None] = None,
        filters: Union[dict, None] = None,
    ) -> list[Shrub]:
        """Retrieves a list of shrubs from a specified endpoint using provided parameters.

        Args:
            limit (int, str None): The maximum number of shrubs to return.
                If not provided, defaults to None.
            q (str, None) Search query to filter shrubs by. If not provided, defaults to None.
            filters (dict, None): Additional filters to apply to the search.
                If not provided, defaults to None.

        Returns:
            list[Shrub]: A list of Shrub objects.
        """
        url = Mermaid._build_url(
            endpoint="datastore_search",
            resource_id="0b1af81f-247d-4266-9823-693858ad5b5d",
            limit=limit,
            q=q,
            filters=filters,
        )

        response = await self._get_data(url)
        response = response["result"]["records"]

        return [
            Shrub(
                x_wgs84=x["x_wgs84"],
                y_wgs84=x["y_wgs84"],
                x_pl2000=x["x"],
                y_pl2000=x["y"],
                inventory_number=x["numer_inw"],
                district=x["dzielnica"],
                administrative_unit=x["jednostka"],
                city=x["miasto"],
                address=x["adres"],
                location=x["lokalizacja"],
                spacies_polish=x["gatunek"],
                spacies_latin=x["gatunek1"],
                measurement_date=x["data_wyk_pom"],
                age=x["wiek_w_dni"],
                health=x["stan_zdrowia"],
            )
            for x in response
        ]

    async def get_shrubs_groups(
        self,
        limit: Union[int, str, None] = None,
        q: Union[str, None] = None,
        filters: Union[dict, None] = None,
    ):
        """Retrieves a list of shrubs groups from a specified endpoint using provided parameters.

        Args:
            limit (int, str, None): The maximum number of shrubs groups to return.
                If not provided, defaults to None.
            q (str, None) Search query to filter shrubs groups by.
                If not provided, defaults to None.
            filters (dict, None): Additional filters to apply to the search.
                If not provided, defaults to None.

        Returns:
            list[ShrubsGroup]: A list of ShrubsGroup objects.
        """
        url = Mermaid._build_url(
            endpoint="datastore_search",
            resource_id="4b792a76-5349-4aad-aa16-dadaf0a74be3",
            limit=limit,
            q=q,
            filters=filters,
        )
        response = await self._get_data(url)
        response = response["result"]["records"]

        return [
            ShrubsGroup(
                x_wgs84=x["x_wgs84"],
                y_wgs84=x["y_wgs84"],
                x_pl2000=x["x_pl2000"],
                y_pl2000=x["y_pl2000"],
                outline_id=x["id_obrysu"],
                outline_partid=x["partid_obrysu"],
                inventory_number=x["numer_inw"],
                district=x["dzielnica"],
                administrative_unit=x["jednostka"],
                city=x["miasto"],
                address=x["adres"],
                location=x["lokalizacja"],
                spacies=x["gatunki"],
                measurement_date=x["data_wyk_pom"],
                age=x["wiek_w_dni"],
                area=x["powierzchnia"],
                height=x["wysokosc"],
                health=x["stan_zdrowia"],
            )
            for x in response
        ]

    async def get_forests(
        self,
        limit: Union[int, str, None] = None,
        q: Union[str, None] = None,
        filters: Union[dict, None] = None,
    ):
        """Retrieves a list of forests from a specified endpoint using provided parameters.

        Args:
            limit (int, str, None): The maximum number of forests to return.
                If not provided, defaults to None.
            q (str, None): Search query to filter forest by.
                If not provided, defaults to None.
            filters (dict, None): Additional filters to apply to the search.
                If not provided, defaults to None.

        Returns:
            list[Forest]: A list of Forest objects.
        """
        url = Mermaid._build_url(
            endpoint="datastore_search",
            resource_id="75bedfd5-6c83-426b-9ae5-f03651857a48",
            limit=limit,
            q=q,
            filters=filters,
        )
        response = await self._get_data(url)
        response = response["result"]["records"]

        return [
            Forest(
                x_wgs84=x["x_wgs84"],
                y_wgs84=x["y_wgs84"],
                x_pl2000=x["x_pl2000"],
                y_pl2000=x["y_pl2000"],
                identifier=x["id"],
                partid=x["partid"],
                district=x["dzielnica"],
                forest_district=x["obwód"],
                estate=x["osiedle"],
                unit_number=x["nr_oddz"],
                sub_unit_number=x["poddz"],
                area=x["powierzchnia"],
                habitat_type=x["stl"],
                ecosystem_layer=x["powierzchnia1"],
                dominant_spacies=x["gat_panujacy"],
                surface_share=x["udział"],
                age=x["wiek"],
                bonitation=x["bonitacja"],
                woodlot=x["zadrzewienie"],
                density=x["zwarcie"],
                mixing=x["zmieszanie"],
                sapling=x["podrost"],
                underbrush=x["podszyt"],
                plan_type=x["typ_planu"],
                plan=x["planu"],
                plan_duration=x["obowiazywanie"],
                shape_area=x["shape_area"],
                shape_len=x["shape_len"],
            )
            for x in response
        ]

    async def get_trees(
        self,
        limit: Union[int, str, None] = None,
        q: Union[str, None] = None,
        filters: Union[dict, None] = None,
    ):
        """Retrieves a list of trees from a specified endpoint using provided parameters.

        Args:
            limit (int, str, None): The maximum number of trees to return.
                If not provided, defaults to None.
            q (str, None): Search query to filter trees by.
                If not provided, defaults to None.
            filters (dict, None): Additional filters to apply to the search.
                If not provided, defaults to None.

        Returns:
            list[Tree]: A list of trees objects.
        """
        url = Mermaid._build_url(
            endpoint="datastore_search",
            resource_id="ed6217dd-c8d0-4f7b-8bed-3b7eb81a95ba",
            limit=limit,
            q=q,
            filters=filters,
        )
        response = await self._get_data(url)
        response = response["result"]["records"]

        return [
            Tree(
                x_wgs84=x["x_wgs84"],
                y_wgs84=x["y_wgs84"],
                x_pl2000=x["x_pl2000"],
                y_pl2000=x["y_pl2000"],
                inventory_number=x["numer_inw"],
                district=x["dzielnica"],
                administrative_unit=x["jednostka"],
                city=x["miasto"],
                address=x["adres"],
                house_number=x["numer_adres"],
                location=x["lokalizacja"],
                spacies_polish=x["gatunek"],
                spacies_latin=x["gatunek_1"],
                measurement_date=x["data_wyk_pom"],
                age=x["wiek_w_dni"],
                height=x["wysokosc"],
                trunk_circumference=x["pnie_obwod"],
                crown_diameter=x["srednica_k"],
                health=x["stan_zdrowia"],
            )
            for x in response
        ]

    async def get_trees_groups(
        self,
        limit: Union[int, str, None] = None,
        q: Union[str, None] = None,
        filters: Union[dict, None] = None,
    ):
        """Retrieves a list of trees groups from a specified endpoint using provided parameters.

        Args:
            limit (int, str, None): The maximum number of trees groups to return.
                If not provided, defaults to None.
            q (str, None): Search query to filter trees groups by.
                If not provided, defaults to None.
            filters (dict, None): Additional filters to apply to the search.
                If not provided, defaults to None.

        Returns:
            list[TreesGroup]: A list of trees groups objects.
        """
        url = Mermaid._build_url(
            endpoint="datastore_search",
            resource_id="913856f7-f71b-4638-abe2-12df14334e1a",
            limit=limit,
            q=q,
            filters=filters,
        )

        response = await self._get_data(url)
        response = response["result"]["records"]

        return [
            TreesGroup(
                x_wgs84=x["x_wgs84"],
                y_wgs84=x["y_wgs84"],
                x_pl2000=x["x_pl2000"],
                y_pl2000=x["y_pl2000"],
                inventory_number=x["numer_inw"],
                outline_id=x["id_obrysu"],
                outline_partid=x["partid_obrysu"],
                district=x["dzielnica"],
                administrative_unit=x["jednostka"],
                city=x["miasto"],
                address=x["adres"],
                location=x["lokalizacja"],
                spacies=x["gatunki"],
                measurement_date=x["data_wyk_pom"],
                health=x["stan_zdrowia"],
            )
            for x in response
        ]

    async def get_munincipal_waste(
        self,
        limit: Union[int, str, None] = None,
        q: Union[str, None] = None,
        filters: Union[dict, None] = None,
    ):
        """Retrieves a list of munincipal wastes from a specified endpoint using provided parameters.

        Args:
            limit (int, str, None): The maximum number of munincipal wastes to return.
                If not provided, defaults to None.
            q (str, None): Search query to filter munincipal wastes by.
                If not provided, defaults to None.
            filters (dict, None): Additional filters to apply to the search.
                If not provided, defaults to None.

        Returns:
            list[MunincipalWaste]: A list of munincipal wastes objects.
        """
        url = Mermaid._build_url(
            endpoint="datastore_search",
            resource_id="64b9d66c-d134-4a87-9f24-258676e9e498",
            limit=limit,
            q=q,
            filters=filters,
        )

        response = await self._get_data(url)
        response = response["result"]["records"]

        return [
            MunincipalWaste(
                identifier=x["Identyfikator"],
                name=x["Nazwa"],
                synonym=x["Synonim"],
                waste_type=x["Typ"],
                description=x["Opis"],
                yes=x["Tak"],
                no=x["Nie"],
            )
            for x in response
        ]

    async def get_air_quality(self) -> list[AirQuality]:
        """Retrieves a list of air quality objects from specified endpoint.

        Returns:
            list[AirQuality]: A list of air quulity objects.
        """
        url = Mermaid._build_url(
            endpoint="air_sensors_get",
            apikey=self.api_key,
        )
        response = await self._get_data(url)
        response = response["result"]

        return [
            AirQuality(
                ijp=Ijp(
                    name=x["ijp"]["name"], recommendations=x["ijp"]["recommendations"]
                ),
                data_source=x["data_source"],
                name=x["name"],
                station_type=x["station_type"],
                lon=x["lon"],
                lat=x["lat"],
                owner=x["owner"],
                station=x["station"],
                address=AirStationAddress(
                    city=x["address"]["city"],
                    street=x["address"]["street"],
                    zip_code=x["address"]["zip_code"],
                    district=x["address"]["district"],
                    commune=x["address"]["commune"],
                ),
                data=[
                    AirData(
                        ijp=Ijp(name=y["ijp"]["name"]),
                        param_name=y["param_name"],
                        param_code=y["param_code"],
                        value=y["value"],
                        time=y["time"],
                        unit=y["unit"],
                    )
                    for y in x["data"]
                ],
            )
            for x in response
        ]

    async def get_defibrillators(self, defibrillator_id: Union[int, str, None] = None):
        """Retrieves a list of defibrillators from a specified endpoint using provided parameters

        Args:
            defibrillator_id (int, str, None): An id of defibrillator to search
                If provided, the response contains attachement with the photo encoded in Base64.

        Returns:
            list[Defibrillator]: A list of defibrillator objects.

        """
        url = Mermaid._build_url(
            endpoint="aed_get", apikey=self.api_key, defibrillator_id=defibrillator_id
        )

        response = await self._get_data(url)
        response = response["result"]

        return [
            Defibrillator(
                geometry=DefibrillatorGeometry(
                    map_type=x["geometry"]["type"],
                    coordinates=[y for y in x["geometry"]["coordinates"]],
                ),
                properties=DefibrillatorProperties(
                    device_manufacturer=x["properties"]["device_manufacturer"],
                    device_public_access=x["properties"]["device_public_access"],
                    location_building=x["properties"]["location_building"],
                    location_city=x["properties"]["location_city"],
                    location_description=x["properties"]["location_description"],
                    location_object_name=x["properties"]["location_object_name"],
                    location_postcode=x["properties"]["location_postcode"],
                    location_street=x["properties"]["location_street"],
                    attachment=x["properties"]["attachment"]
                    if defibrillator_id
                    else None,
                ),
            )
            for x in response
        ]

    async def get_vehicle_location(
        self,
        vehicle_type: Union[int, str],
        line: Union[int, str, None] = None,
        brigade: Union[int, str, None] = None,
    ):
        """Retrieves a list of objects with the current public transpor vehicle location.

        Args:
            vehicle_type (int, str): 1 - bus, 2 - tram
            line (int, str, None): Number of the public transport line
            brigade (int, str, None): Number of the public transport brigade

        Returns:
            list[VehicleLocation]: A list of vehicle location objects.
        """
        url = Mermaid._build_url(
            endpoint="busestrams_get",
            resource_id="f2e5503e-927d-4ad3-9500-4ab9e55deb59",
            apikey=self.api_key,
            type=vehicle_type,
            line=line,
            brigade=brigade,
        )

        response = await self._get_data(url)
        response = response["result"]

        return [
            VehicleLocation(
                lat=x["Lat"],
                lon=x["Lon"],
                time=x["Time"],
                lines=x["Lines"],
                brigade=x["Brigade"],
                vehicle_number=x["VehicleNumber"],
            )
            for x in response
        ]

    async def get_stop_set(self, stop_name: str):
        """Retrieves a list of the public transport stops sets for the provided public transport stop.

        Args:
            stop_name (str): Name of the public transport stop

        Returns:
            list[StopSet]: A list of stop set objects.
        """
        url = Mermaid._build_url(
            endpoint="dbtimetable_get",
            id="b27f4c17-5c50-4a5b-89dd-236b282bc499",
            name=stop_name,
            apikey=self.api_key,
        )

        response = await self._get_data(url)
        response = response["result"][0]["values"]

        return StopSet(stop_name=response[1]["value"], set_number=response[0]["value"])

    async def get_stop_lines(self, busstop_id: Union[int, str], busstop_number: str):
        """Retrieves a list of the public transport line for the provided public transport stop.

        Args:
            busstop_id (int, str): Public transport stop id
            busstop_nubmer (str): Stop bar ID (eg. 01, 02)

        Returns:
            list[StopLine]: A list of stop line objects.

        """
        url = Mermaid._build_url(
            endpoint="dbtimetable_get",
            id="88cd555f-6f31-43ca-9de4-66c479ad5942",
            busstopId=busstop_id,
            busstopNr=busstop_number,
            apikey=self.api_key,
        )
        """ """

        response = await self._get_data(url)
        response = response["result"]

        return [StopLine(line_number=x["values"][0]["value"]) for x in response]

    async def get_line_timetable(
        self, busstop_id: Union[int, str], busstop_number: str, line: Union[int, str]
    ):
        """Retrieves a list of the line timetable for the provided public transport stop and line.

        Args:
            busstop_id (int, str): Public transport stop id
            busstop_nubmer (str): Stop bar ID (eg. 01, 02)
            line: Public transport line number

        Returns:
            list[LineTimetable]: A list of line timetable objects.

        """
        url = Mermaid._build_url(
            endpoint="dbtimetable_get",
            id="e923fa0e-d96c-43f9-ae6e-60518c9f3238",
            busstopId=busstop_id,
            busstopNr=busstop_number,
            line=line,
            apikey=self.api_key,
        )

        response = await self._get_data(url)
        response = [x["values"] for x in response["result"]]
        response = [{y["key"]: y["value"] for y in x} for x in response]

        return [
            LineTimetable(
                brigade=x["brygada"],
                direction=x["kierunek"],
                route=x["trasa"],
                time=x["czas"],
                symbol_1=x["symbol_1"],
                symbol_2=x["symbol_2"],
            )
            for x in response
        ]

    async def get_cycle_tracks(
        self,
        limit: Union[int, str, None] = None,
        bbox: Union[str, None] = None,
        circle: Union[str, None] = None,
        query_filter: Union[str, None] = None,
    ):
        """Retrieves a list of cycle tracks.

        Args:
            limit (int, str, None): The maximum number of tracks to return.
                If not provided, defaults to None.
            bbox (str, None): Coordinates (min_lol, min_lat, max_lon, max lat)
                of the search area defined by a rectangle. In not provided, defaults to None.
            circle(str, None) Coordinates of the center of a circular area and its radius in meters.
                If not provided, defaults to None.
            query_filter (str, None): a special XML format used to filter query results.

        Returns:
            list[CycleTrack]: A list of cycle track objects.

        """
        url = Mermaid._build_url(
            endpoint="wfsstore_get",
            id="8a235d27-b96a-4876-9b92-9e164940c9b6",
            limit=limit,
            bbox=bbox,
            circle=circle,
            filter=query_filter,
            apikey=self.api_key,
        )

        response = await self._get_data(url)
        response = response["result"]["featureMemberProperties"]
        return [
            CycleTrack(
                location=x["LOKALIZ"],
                route_type=x["TYP_TRASY"],
                district=x["DZIELNICA"],
                object_id=x["OBJECTID"],
                surface_type=x["TYP_NAW"],
            )
            for x in response
        ]

    async def get_cycle_stations(
        self,
        limit: Union[int, str, None] = None,
        bbox: Union[str, None] = None,
        circle: Union[str, None] = None,
        query_filter: Union[str, None] = None,
    ):
        """Retrieves a list of cycle stations.

        Args:
            limit (int, str, None): The maximum number of stations to return.
                If not provided, defaults to None.
            bbox (str, None): Coordinates (min_lol, min_lat, max_lon, max lat)
                of the search area defined by a rectangle. In not provided, defaults to None.
            circle(str, None) Coordinates of the center of a circular area and its radius in meters.
                If not provided, defaults to None.
            query_filter (str, None): a special XML format used to filter query results.

        Returns:
            list[CycleStation]: A list of cycle stations objects.

        """
        url = Mermaid._build_url(
            endpoint="wfsstore_get",
            id="a08136ec-1037-4029-9aa5-b0d0ee0b9d88",
            limit=limit,
            bbox=bbox,
            circle=circle,
            filter=query_filter,
            apikey=self.api_key,
        )

        response = await self._get_data(url)
        response = response["result"]["featureMemberProperties"]

        return [
            CycleStation(
                racks=x["STOJAKI"],
                update_date=x["AKTU_DAN"],
                object_id=x["OBJECTID"],
                location=x["LOKALIZACJA"],
                bikes=x["ROWERY"],
                station_number=x["NR_STACJI"],
            )
            for x in response
        ]

    async def get_parking_lots(
        self,
        limit: Union[int, str, None] = None,
        bbox: Union[str, None] = None,
        circle: Union[str, None] = None,
        query_filter: Union[str, None] = None,
    ):
        """Retrieves a list of parking lots.

        Args:
            limit (int, str, None): The maximum number of parking lots to return.
                If not provided, defaults to None.
            bbox (str, None): Coordinates (min_lol, min_lat, max_lon, max lat)
                of the search area defined by a rectangle. In not provided, defaults to None.
            circle(str, None) Coordinates of the center of a circular area and its radius in meters.
                If not provided, defaults to None.
            query_filter (str, None): a special XML format used to filter query results.

        Returns:
            list[ParkingLot]: A list of parking lot objects.

        """
        url = Mermaid._build_url(
            endpoint="wfsstore_get",
            id="157648fd-a603-4861-af96-884a8e35b155",
            limit=limit,
            bbox=bbox,
            circle=circle,
            filter=query_filter,
            apikey=self.api_key,
        )

        response = await self._get_data(url)
        response = response["result"]["featureMemberProperties"]

        return [
            ParkingLot(
                disabled_parking_places=x["NIEPELNO"],
                motorcycle_places=x["MOTORY"],
                car_places=x["AUTA"],
                description=x["OPIS"],
                object_id=x["OBJECTID"],
                name=x["NAZWA"],
                update_date=x["AKTU_DAN"],
            )
            for x in response
        ]

    async def get_subway_entrances(
        self,
        limit: Union[int, str, None] = None,
        bbox: Union[str, None] = None,
        circle: Union[str, None] = None,
        query_filter: Union[str, None] = None,
    ):
        """Retrieves a list of subway entrances.

        Args:
            limit (int, str, None): The maximum number of entrances to return.
                If not provided, defaults to None.
            bbox (str, None): Coordinates (min_lol, min_lat, max_lon, max lat)
                of the search area defined by a rectangle. In not provided, defaults to None.
            circle(str, None) Coordinates of the center of a circular area and its radius in meters.
                If not provided, defaults to None.
            query_filter (str, None): a special XML format used to filter query results.

        Returns:
            list[SubwayEntrance]: A list of subway entrance objects.

        """
        url = Mermaid._build_url(
            endpoint="wfsstore_get",
            id="0ac7f6d1-a26b-430f-9e3d-a41c5356b9a3",
            limit=limit,
            bbox=bbox,
            circle=circle,
            filter=query_filter,
            apikey=self.api_key,
        )

        response = await self._get_data(url)
        response = response["result"]["featureMemberProperties"]

        return [SubwayEntrance(object_id=x["OBJECTID"]) for x in response]

    async def get_stop_info(
        self,
        page: Union[int, str, None] = None,
        size: Union[int, str, None] = None,
        sort_by: Union[str, None] = None,
        current_day: bool = False,
    ):
        """Retrieves a bus stops information.

        Args:
            page (int, str, None): Page. If not provided, defaults to None.
            size (int, str, None): Size. If not provided, defaults to None.
            sort_by (str, None): A field to sort by. If not provided, defaults to None.
            current_day (bool): Return an information for a current day only.
                If not provided, defaults to False.

        Returns:
            list[StopInfo]: List of stop info objects.

        """
        res_id = (
            "ab75c33d-3a26-4342-b36a-6e5fef0a3ac3"
            if not current_day
            else "1c08a38c-ae09-46d2-8926-4f9d25cb0630"
        )

        url = Mermaid._build_url(
            endpoint="dbstore_get",
            id=res_id,
            page=page,
            size=size,
            sortBy=sort_by,
            apikey=self.api_key,
        )

        response = await self._get_data(url)
        response = [x["values"] for x in response["result"]]
        response = [{y["key"]: y["value"] for y in x} for x in response]

        return [
            StopInfo(
                set_number=x["zespol"],
                bar=x["slupek"],
                set_name=x["nazwa_zespolu"],
                street_id=x["id_ulicy"],
                lat=x["szer_geo"],
                lon=x["dlug_geo"],
                direction=x["kierunek"],
                valid_from=x["obowiazuje_od"],
            )
            for x in response
        ]

    async def get_theaters(
        self,
        limit: Union[int, str, None] = None,
        bbox: Union[str, None] = None,
        circle: Union[str, None] = None,
        query_filter: Union[str, None] = None,
    ):
        """Retrieves a list of theaters.

        Args:
            limit (int, str, None): The maximum number of theaters to return.
                If not provided, defaults to None.
            bbox (str, None): Coordinates (min_lol, min_lat, max_lon, max lat)
                of the search area defined by a rectangle. In not provided, defaults to None.
            circle(str, None) Coordinates of the center of a circular area and its radius in meters.
                If not provided, defaults to None.
            query_filter (str, None): a special XML format used to filter query results.

        Returns:
            list[Theather]: A list of theaters objects.

        """

        url = Mermaid._build_url(
            endpoint="wfsstore_get",
            id="e26218cb-61ec-4ccb-81cc-fd19a6fee0f8",
            limit=limit,
            bbox=bbox,
            circle=circle,
            filter=query_filter,
            apikey=self.api_key,
        )

        response = await self._get_data(url)
        response = response["result"]["featureMemberProperties"]

        return [
            Theater(
                phone_number_or_fax=x["TEL_FAX"],
                website=x.get("WWW"),
                administrative_unit=x.get("JEDN_ADM"),
                update_date=x["AKTU_DAN"],
                object_id=x["OBJECTID"],
                number=x["NUMER"],
                postcode=x["KOD"],
                description=x["OPIS"],
                street=x["ULICA"],
                district=x["DZIELNICA"],
                mail=x.get("MAIL"),
            )
            for x in response
        ]

    async def get_internet_access(
        self,
        limit: Union[int, str, None] = None,
        q: Union[str, None] = None,
        filters: Union[dict, None] = None,
    ):
        """Retrieves an internet access of schools information.

        Args:
            limit (int, str, None): The maximum number of objects to return.
                If not provided, defaults to None
            q (str, None): Search query to filter objects by.
                If not provided, defaults to None.
            filters (dict, None): Additional filters to apply to the search.
                If not provided, defaults to None.

        Returns:
            list[InternetAccess]: A list of internet access objects.
        """
        url = Mermaid._build_url(
            endpoint="datastore_search",
            resource_id="0a131e16-ec7f-4502-9b62-8f8af58d8cfd",
            limit=limit,
            q=q,
            filters=filters,
        )

        response = await self._get_data(url)
        response = response["result"]["records"]

        return [
            InternetAccess(
                school_number=x["Nr RSPO"],
                school_type=x["Typ szkoły/placówki"],
                school_name=x["Nazwa szkoły/placówki"],
                telephone_link_up_to_1=x["Łącze telefoniczne - do 1 Mbit"],
                telephone_link_up_to_2=x["Łącze telefoniczne - do 2 Mbit"],
                telephone_link_up_to_10=x["Łącze telefoniczne - do 10 Mbit"],
                telephone_link_above_10=x["Łącze telefoniczne - powyżej 10 Mbit"],
                tv_link_up_to_1=x["łącze TV - do 1 Mbit"],
                tv_link_up_to_2=x["łącze TV - do 2 Mbit"],
                tv_link_up_to_10=x["łącze TV - do 10 Mbit"],
                tv_link_above_10=x["łącze TV - powyżej 10 Mbit"],
                fiber_optics_up_to_1=x["Światłowód - do 1 Mbit"],
                fiber_optics_up_to_2=x["Światłowód - do 2 Mbit"],
                fiber_optics_up_to_10=x["Światłowód - do 10 Mbit"],
                fiber_optics_above_10=x["Światłowód - do 10 Mbit"],
                sat_link_up_to_1=x["Łącze SAT -do 1 Mbit"],
                sat_link_up_to_2=x["Łącze SAT - do 2 Mbit"],
                sat_link_up_to_10=x["Łącze SAT - do 10 Mbit"],
                sat_link_above_10=x["Łącze SAT - powyżej 10 Mbit"],
                radio_link_up_to_1=x["Łącze radio - do 1 Mbit"],
                radio_link_up_to_2=x["Łącze radio - do 2 Mbit"],
                radio_link_up_to_10=x["Łącze radio - do 10 Mbit"],
                radio_link_above_10=x["Łącze radio - powyżej 10 Mbit"],
                mobile_phone_link_up_to_1=x["Łącze tel kom - do 1 Mbit"],
                mobile_phone_link_up_to_2=x["Łącze tel kom - do 2 Mbit"],
                mobile_phone_link_up_to_10=x["Łącze tel kom - do 10 Mbit"],
                mobile_phone_link_above_10=x["Łącze tel kom - powyżej 10 Mbit"],
                province=x["Województwo"],
                county=x["Powiat"],
                munincipality=x["Gmina"],
                location=x["Miejscowość"],
                street=x["Ulica"],
                house_number=x["Nr domu"],
                apartment_number=x["Nr mieszkania"],
                postal_code=x["Kod pocztowy"],
                post_office=x["Poczta"],
                phone=x["Telefon"],
                email=x["E-mail"],
                governing_body_type=x["Typ organu prowadzącego"],
                audience=x["Publiczność"],
                student_category=x["Kategoria uczniów"],
                school_specificity=x["Specyfika szkoły"],
                institution_type=x["Rodzaj placówki"],
            )
            for x in response
        ]

    async def get_computers_purpose(
        self,
        limit: Union[int, str, None] = None,
        q: Union[str, None] = None,
        filters: Union[dict, None] = None,
    ):
        """Retrieves a purposes of computers in schools.

        Args:
            limit (int, str, None): The maximum number of objects to return.
                If not provided, defaults to None
            q (str, None): Search query to filter objects by.
                If not provided, defaults to None.
            filters (dict, None): Additional filters to apply to the search.
                If not provided, defaults to None.

        Returns:
            list[ComputerPurpose]: A list of internet access objects.
        """
        url = Mermaid._build_url(
            endpoint="datastore_search",
            resource_id="e22be977-f15d-42e6-843a-55fd0a0d756e",
            limit=limit,
            q=q,
            filters=filters,
        )

        response = await self._get_data(url)
        response = response["result"]["records"]

        return [
            ComputerPurpose(
                school_number=x["Nr RSPO"],
                school_type=x["Typ szkoły/placówki"],
                school_name=x["Nazwa szkoły/placówki"],
                total_teaching=x["dydaktyka ogółem"],
                teaching_with_internet_access=x["dydaktyka z dostępem do internetu"],
                portable_teaching=x["dydaktyka  przenośne"],
                total_teaching_in_library=x["z tego w bibliotece - ogółem"],
                total_with_internet_access_in_library=x[
                    "z tego w bibliotece - z dostępem do internetu"
                ],
                teaching_portable_in_library=x["z tego w bibliotece - przenośne"],
                total_teaching_available_for_students=x[
                    "z tego dostępne dla uczniów - ogółem"
                ],
                total_with_internet_access_available_for_students=x[
                    "z tego dostępne dla uczniów - z dostępem do internetu"
                ],
                teaching_portable_available_for_students=x[
                    "z tego dostępne dla uczniów - przenośne"
                ],
                other_total=x["pozostałe - ogółem"],
                other_with_internet_access=x["pozostałe - z dostępem do internetu"],
                other_portable=x["pozostałe - przenośne"],
                province=x["Województwo"],
                county=x["Powiat"],
                munincipality=x["Gmina"],
                location=x["Miejscowość"],
                street=x["Ulica"],
                house_number=x["Nr domu"],
                apartment_number=x["Nr mieszkania"],
                postal_code=x["Kod pocztowy"],
                post_office=x["Poczta"],
                phone=x["Telefon"],
                email=x["E-mail"],
                governing_body_type=x["Typ organu prowadzącego"],
                audience=x["Publiczność"],
                student_category=x["Kategoria uczniów"],
                school_specificity=x["Specyfika szkoły"],
                institution_type=x["Rodzaj placówki"],
            )
            for x in response
        ]
