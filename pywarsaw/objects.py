import datetime
import json
from typing import Union

from attrs import define, field, asdict, astuple, converters

from .utils import (
    flat_dict,
    to_date,
    to_datetime,
    to_time,
    comma_number_to_float,
    to_datetime_with_12,
)


class JSONEncoder(json.JSONEncoder):
    """Custom json encoder to deal with dates, times and DTOs"""

    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.time)):
            return obj.isoformat()
        elif isinstance(obj, DTO):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)


# Data transfer object


@define
class DTO:
    """Parent class for all DTOs"""

    def to_dict(self) -> dict:
        """Convert object to a dictionary"""
        return asdict(self)

    def to_flat_dict(self) -> dict:
        """Convert object to a flat dictionary"""
        d = asdict(self)
        return flat_dict(d)

    def to_tuple(self) -> tuple:
        """Convert object to a tuple"""
        return astuple(self)

    def to_json(self) -> str:
        """Convert object to a json string"""
        return JSONEncoder().encode(self)


# @define
# class Theater(DTO):
#     object_id: str
#     number: str
#     phone_fax: str
#     website: Optional[str] = None
#     administrative_unit: str
#     # to do


# ECOLOGY OBJECTS


@define
class Shrub(DTO):
    """
    Individual shrub.

    The following information is available:
        * x_wgs84: x coordinate in WGS84 (EPSG:4326) coordinate system
        * y_wgs84: y coordinate in WGS84 (EPSG:4326) coordinate system
        * x_pl2000: x coordinate in PUWG2000 (EPSG: 2178) coordinate system
        * y_pl2000: y coordinate in PUWG2000 (EPSG: 2178) coordinate system
        * inventory_number: inventory number
        * district: district
        * administrative_unit: administrative unit
        * city: city
        * address: address
        * location: location
        * spacies_polish: species description in Polish
        * spacies_latin: species description in Latin
        * measurement_date: measurement date
        * age: plant age in days
        * health: plant condition
    """

    x_wgs84: Union[int, float]
    y_wgs84: Union[int, float]
    x_pl2000: Union[int, float]
    y_pl2000: Union[int, float]
    inventory_number: str
    district: str
    administrative_unit: str
    city: str
    address: str
    location: str
    spacies_polish: str
    spacies_latin: str
    measurement_date: Union[datetime.date, None] = field(converter=to_date)
    age: int
    health: str


@define
class ShrubsGroup(DTO):
    """
    Group of shrubs.

    The following information is available:
        * x_wgs84: x coordinate of the outline point in WGS84 (EPSG:4326) coordinate system
        * y_wgs84: y coordinate of the outline point in WGS84 (EPSG:4326) coordinate system
        * x_pl2000: x coordinate of the outline point in PUWG2000 (EPSG: 2178) coordinate system
        * y_pl2000: y coordinate of the outline point in PUWG2000 (EPSG: 2178) coordinate system
        * outline_id: outline identifier
        * outline_partid: outline part identifier
        * inventory_number: inventory number
        * district: district
        * administrative_unit: administrative unit
        * city: city
        * adres: address
        * location: location
        * spacies: species description in Polish and Latin
        * measurement_date: measurement date
        * age: plant age in days
        * area: occupied area in square meters
        * height: height of a group of bushes in meters
        * health: plant condition (good, average, bad)
    """

    x_wgs84: Union[int, float]
    y_wgs84: Union[int, float]
    x_pl2000: Union[int, float]
    y_pl2000: Union[int, float]
    outline_id: int
    outline_partid: int
    inventory_number: str
    district: str
    administrative_unit: str
    city: str
    address: str
    location: str
    spacies: str
    measurement_date: Union[datetime.date, None] = field(converter=to_date)
    age: int
    area: Union[float, str] = field(converter=comma_number_to_float)
    height: float = field(converter=comma_number_to_float)
    health: str


@define
class Forest(DTO):
    """
    Forest.

    The following information is available:
        * x_wgs84 - the x coordinate in WGS84 (EPSG:4326)
        * y_wgs84 - the y coordinate in WGS84 (EPSG:4326)
        * x_pl2000 - the x coordinate in PUWG2000 (EPSG:2178)
        * y_pl2000 - the y coordinate in PUWG2000 (EPSG:2178)
        * identifier - area identifier
        * partid - part identifier
        * district - name of the city district
        * forest_district - name of the forest district
        * estate - residential area in the city
        * unit_number - number of the forest division
        * sub_unit_number - number of the forest sub-division
        * area - area of the division
        * habitat_type - type of forest habitat
        * ecosystem_layer - layer of the forest ecosystem
        * dominant_spacies - dominant tree species
        * surface_share - share of the species' area
        * age - age in years
        * bonitation - indicator of the habitat's productive capacity
        * woodlot - indicator of the coverage of the area with forest vegetation for the tree stand
        * density - degree of forest density
        * mixing - degree of forest mixing
        * sapling - characteristic of the shrub layer
        * underbrush - layer of shrubs and trees not belonging to the upper floor of the tree stand
        * plan_type - type of forest management plan
        * plan - description of the forest management plan
        * plan_duration - period of validity of the plan
        * shape_area - shape of the area of the forest division
        * shape_len - length of the area of the forest division
    """

    x_wgs84: Union[int, float]
    y_wgs84: Union[int, float]
    x_pl2000: Union[int, float]
    y_pl2000: Union[int, float]
    identifier: int
    partid: int
    district: str
    forest_district: str
    estate: str
    unit_number: str
    sub_unit_number: str
    area: float = field(converter=comma_number_to_float)
    habitat_type: str
    ecosystem_layer: str
    dominant_spacies: str
    surface_share: Union[float, str] = field(converter=comma_number_to_float)
    age: int
    bonitation: str
    woodlot: Union[float, str] = field(converter=comma_number_to_float)
    density: str
    mixing: str
    sapling: str
    underbrush: str
    plan_type: str
    plan: str
    plan_duration: str
    shape_area: Union[int, float]
    shape_len: Union[int, float]


@define
class Tree(DTO):
    """
    Invidual tree.

    The following information is available:
        * x_wgs84: x coordinate in WGS84 (EPSG:4326) coordinate system
        * y_wgs84: y coordinate in WGS84 (EPSG:4326) coordinate system
        * x_pl2000: x coordinate in PUWG2000 (EPSG: 2178) coordinate system
        * y_pl2000: y coordinate in PUWG2000 (EPSG: 2178) coordinate system
        * inventory_number: inventory number
        * district: district
        * administrative_unit: administrative unit
        * city: city
        * address: address
        * house_number: house number
        * location: location
        * spacies_polish: species description in Polish
        * spacies_latin: species description in Latin
        * measurement_date: measurement date
        * age: plant age in days
        * height: height in meters
        * trunk_circumference: trunk circumference
        * crown_diameter: crown diameter
        * health: plant condition
    """

    x_wgs84: Union[int, float]
    y_wgs84: Union[int, float]
    x_pl2000: Union[int, float]
    y_pl2000: Union[int, float]
    inventory_number: str
    district: str
    administrative_unit: str
    city: str
    address: str
    house_number: str
    location: str
    spacies_polish: str
    spacies_latin: str
    measurement_date: Union[datetime.date, None] = field(converter=to_date)
    age: int
    height: float = field(converter=comma_number_to_float)
    trunk_circumference: float = field(converter=comma_number_to_float)
    crown_diameter: float = field(converter=comma_number_to_float)
    health: str


@define
class TreesGroup(DTO):
    """
    Group of trees.

    The following information is available:
        * x_wgs84: x coordinate of the outline point in WGS84 (EPSG:4326) coordinate system
        * y_wgs84: y coordinate of the outline point in WGS84 (EPSG:4326) coordinate system
        * x_pl2000: x coordinate of the outline point in PUWG2000 (EPSG: 2178) coordinate system
        * y_pl2000: y coordinate of the outline point in PUWG2000 (EPSG: 2178) coordinate system
        * outline_id: outline identifier
        * outline_partid: outline part identifier
        * inventory_number: inventory number
        * district: district
        * administrative_unit: administrative unit
        * city: city
        * address: address
        * location: location
        * spacies: species description in Polish and Latin
        * measurement_date: measurement date
        * health: plant condition
    """

    x_wgs84: Union[int, float]
    y_wgs84: Union[int, float]
    x_pl2000: Union[int, float]
    y_pl2000: Union[int, float]
    inventory_number: str
    outline_id: int
    outline_partid: int
    district: str
    administrative_unit: str
    city: str
    address: str
    location: str
    spacies: str
    measurement_date: Union[datetime.date, None] = field(converter=to_date)
    health: str


@define
class MunincipalWaste(DTO):
    """
    Munincipal waste.

    The following information is available:
        * identifier: verification identifier (unique numerical value)
        * name: waste name (string of characters)
        * synonym: synonym of waste name (string of characters, synonyms separated by commas)
        * waste_type: waste classification (string of characters)"
        * description - waste description
        * yes: an example of thing in this type
        * no: an example of thing not in this type
    """

    identifier: int
    name: str
    synonym: str
    waste_type: str
    description: str
    yes: str
    no: str


@define
class Ijp(DTO):
    """
    Air Quality Index object for AirQuality DTO.
    """

    name: Union[str, None] = None
    recommendations: Union[str, None] = None


@define
class AirStationAddress(DTO):
    """
    Station object for AirQuality DTO.
    """

    city: str
    street: str
    zip_code: str
    district: str
    commune: str


@define
class AirData(DTO):
    """
    Measurements for AirQuality DTO.
    """

    ijp: Ijp
    param_name: str
    param_code: str
    value: float
    time: Union[datetime.date, None] = field(converter=to_datetime)
    unit: str


@define
class AirQuality(DTO):
    """
    Air quality.

    The following information is available:
        * ijp: overall air quality index calculated according to the Polish Air Quality Index
            * name: verbal summary of the overall air quality index
            * recommendations: recommendation
        * data_source: measurement source
        * name: id of the station
        * station_type: type of station
        * lon: geographical longitude
        * lat: geographical latitude
        * owner: owner of the station
        * station: name of the station
        * address: station address
            * city: city
            * street: street
            * zip_code: postal code
            * district: district
            * commune: commune
        * data: measurements
            * ijp: air quality index for the measurement
                * name (optional): verbal air quality index for the measurement
            * param_name: name of the pollutant
            * param_code: code of the pollutant
            * value: value of the measurement
            * time: time of the measurement
            * unit: unit of measurement"
    """

    ijp: Ijp
    data_source: str
    name: str
    station_type: str
    lon: float
    lat: float
    owner: str
    station: str
    address: AirStationAddress
    data: AirData


# SECURITY OBJECTS


@define
class DefibrillatorGeometry(DTO):
    """Geometry information for Defibrillator DTO."""

    map_type: str
    coordinates: list[str]


@define
class DefibrillatorProperties(DTO):
    """Properties for Defibrillator DTO."""

    device_manufacturer: str
    device_public_access: str
    location_building: str
    location_city: str
    location_description: str
    location_object_name: str
    location_postcode: str
    location_street: str
    attachment: Union[str, None] = None


@define
class Defibrillator(DTO):
    """Availability of defibrillators.

    The following information is available:
        * geometry:
            * map_type: type of object on the map
            * coordinates: defibrillator's coordinates
        * properties:
            * defibrillator_id: identifier of the defibrillator
            * device_access_description: description of device availability
            * device_availability: information if the device is available 24/7
            * device_location: location of the device
            * device_manufacturer: name of the device manufacturer
            * device_public_access: information about public access to the device
            * location_building: location building number
            * location_city: location city
            * location_description: location description
            * location_object_name: location place
            * location_postcode: location postal code
            * location_street: location street
            * attachment: photo of the defibrillator encoded in Base64
                (only available when defibrillator_id is provided in the query)
    """

    geometry: DefibrillatorGeometry
    properties: DefibrillatorProperties


# TRANSPORT OBJECTS


@define
class VehicleLocation(DTO):
    """The current location of public transport vehicle.

    The following information is available:
        * lat: latitude in WGS84 (EPSG: 4326) coordinate system
        * lon: longtitude in WGS84 (EPSG: 4326) coordinate system
        * time: GPS signal transmission time
        * lines: bus or tram line number
        * brigade: vehicle brigade number
        * vehicle_number: vehicle number
    """

    lat: float
    lon: float
    time: datetime.datetime = field(converter=to_datetime)
    lines: str
    brigade: str
    vehicle_number: str


@define
class StopSet(DTO):
    """Bus/tram stop set.

    The following information is available:
        * stop_name: name of the bus/tram stop
        * set_number: number of the bus/tram stop set
    """

    stop_name: str
    set_number: str


@define
class StopLine(DTO):
    """The line number."""

    line_number: str


@define
class LineTimetable(DTO):
    """The timetable for a public transport line.

    The following information is available:
        * brigade: vehicle brigade number
        * direction: direction
        * route: route
        * time: time of the arrival
        * symbol_1: unknown
        * symbol_2: unknown

    """

    brigade: str
    direction: str
    route: str
    time: datetime.time = field(converter=to_time)
    symbol_1: Union[str, None] = None
    symbol_2: Union[str, None] = None


@define
class CycleTrack(DTO):
    """The bicycle track.

    The following information is available:
        * location: location of the cycle track
        * route_type: type of the route
        * district: district
        * object_id: id of the object
        * surface_type: type of the surface
    """

    location: str
    route_type: str
    district: str
    object_id: str
    surface_type: str


@define
class CycleStation(DTO):
    """The bicycle station.

    The following information is available:
        * racks: count of the racks
        * update_date: date of the data update
        * object_id: id of the object
        * location: location
        * bikes: count of the bikes
        * station_number: station number
    """

    racks: int = field(converter=int)
    update_date: datetime.datetime = field(converter=to_datetime_with_12)
    object_id: str
    location: str
    bikes: int = field(converter=int)
    station_number: str


@define
class ParkingLot(DTO):
    """The car parking.

    The following information is available:
        * disabled_parking_places: number of places for the handicapped people
        * motorcycle_places: number of places for the motorcycles
        * car_places: number of places for the cars
        * description: description
        * object_id: id of the object
        * name: name
        * update_date: date of the data update
    """

    disabled_parking_places: int = field(converter=int)
    motorcycle_places: int = field(converter=int)
    car_places: int = field(converter=int)
    description: str
    object_id: str
    name: str
    update_date: str


@define
class SubwayEntrance(DTO):
    """The subway entrance.

    The following information is available:
        * object_id: id of the object
    """

    object_id: str


@define
class StopInfo(DTO):
    """The information about public transport stop

    The following information is available:
        * set_number: number of the set
        * bar: number of the bar
        * set_name: name of the set
        * street_id: id of the street
        * lat: latitude
        * lon: longitude
        * direction: direction
        * valid_from: effective date
    """

    set_number: str
    bar: str
    set_name: str
    street_id: str
    lat: float = field(converter=float)
    lon: float = field(converter=float)
    direction: str
    valid_from: datetime.datetime = field(converter=to_datetime)


# CULTURE OBJECTS


@define
class Theater(DTO):
    """The theater.

    The following information is available:
        * phone_number_or_fax: phone number or fax
        * website: website
        * administrative_unit: administrative_unit
        * update date: the date of data updateDzielnice
        * object_id: id of the object
        * number: street number
        * postcode: postcode
        * description: description
        * street: street
        * district: district
        * mail: email

    """

    phone_number_or_fax: str
    administrative_unit: str
    update_date: str
    object_id: str
    number: str
    postcode: str
    description: str
    street: str
    district: str
    website: Union[str, None] = None
    mail: Union[str, None] = None


## EDUCATION OBJECTS


@define
class InternetAccess(DTO):
    """The internet access.

    The following information is available:
        * school_number - number of establishments in the Register of Schools and Educational Institutions
        * school_type - e.g. junior high school, adult education center, boarding school
        * school_name - full name, e.g. Non-Public Junior High School No. 1 named after Irena Sendlerowa
        * telephone_link_up_to_1 - up to 1 Mbit - flag (0 - no, 1 - yes)
        * telephone_link_up_to_2 - up to 2 Mbit - flag (0 - no, 1 - yes)
        * telephone_link_up_to_10 - up to 10 Mbit - flag (0 - no, 1 - yes)
        * telephone_link_above_10 - above 10 Mbit - flag (0 - no, 1 - yes)
        * tv_link_up_to_1 - up to 1 Mbit - flag (0 - no, 1 - yes)
        * tv_link_up_to_2 - up to 2 Mbit - flag (0 - no, 1 - yes)
        * tv_link_up_to_10 - up to 10 Mbit - flag (0 - no, 1 - yes)
        * tv_link_above_10 - above 10 Mbit - flag (0 - no, 1 - yes)
        * fiber_optics_up_to_1 - up to 1 Mbit - flag (0 - no, 1 - yes)
        * fiber_optics_up_to_2 - up to 2 Mbit - flag (0 - no, 1 - yes)
        * fiber_optics_up_to_10 - up to 10 Mbit - flag (0 - no, 1 - yes)
        * fiber_optics_above_10 - above 10 Mbit - flag (0 - no, 1 - yes)
        * sat_link_up_to_1 - up to 1 Mbit - flag (0 - no, 1 - yes)
        * sat_link_up_to_2 - up to 2 Mbit - flag (0 - no, 1 - yes)
        * sat_link_up_to_10 - up to 10 Mbit - flag (0 - no, 1 - yes)
        * sat_link_above_10 - above 10 Mbit - flag (0 - no, 1 - yes)
        * radio_link_up_to_1 - up to 1 Mbit - flag (0 - no, 1 - yes)
        * radio_link_up_to_2 - up to 2 Mbit - flag (0 - no, 1 - yes)
        * radio_link_up_to_10 - up to 10 Mbit - flag (0 - no, 1 - yes)
        * radio_link_above_10 - above 10 Mbit - flag (0 - no, 1 - yes)
        * mobile_phone_link_up_to_1 - up to 1 Mbit - flag (0 - no, 1 - yes)
        * mobile_phone_link_up_to_2 - up to 2 Mbit - flag (0 - no, 1 - yes)
        * mobile_phone_link_up_to_10 - up to 10 Mbit - flag (0 - no, 1 - yes)
        * mobile_phone_link_above_10 - above 10 Mbit - flag (0 - no, 1 - yes)
        * province
        * county
        * municipality
        * location
        * street
        * house_number
        * apartment_number
        * postal_code
        * post_office
        * phone
        * email
        * governing_body_type - municipality, city with the rights of a county, foundation, association, individual, non-public higher education institution, commercial company, religious organization
        * audience - public/non-public
        * student_category - children or youth, adults, without category
        * school_specificity - special/no specificity
        * institution_type - independent/composite unit
    """

    school_number: str
    school_type: str
    school_name: str
    telephone_link_up_to_1: [int, None]
    telephone_link_up_to_2: [int, None]
    telephone_link_up_to_10: [int, None]
    telephone_link_above_10: [int, None]
    tv_link_up_to_1: [int, None]
    tv_link_up_to_2: [int, None]
    tv_link_up_to_10: [int, None]
    tv_link_above_10: [int, None]
    fiber_optics_up_to_1: [int, None]
    fiber_optics_up_to_2: [int, None]
    fiber_optics_up_to_10: [int, None]
    fiber_optics_above_10: [int, None]
    sat_link_up_to_1: [int, None]
    sat_link_up_to_2: [int, None]
    sat_link_up_to_10: [int, None]
    sat_link_above_10: [int, None]
    radio_link_up_to_1: [int, None]
    radio_link_up_to_2: [int, None]
    radio_link_up_to_10: [int, None]
    radio_link_above_10: [int, None]
    mobile_phone_link_up_to_1: [int, None]
    mobile_phone_link_up_to_2: [int, None]
    mobile_phone_link_up_to_10: [int, None]
    mobile_phone_link_above_10: [int, None]
    province: str
    county: str
    munincipality: str
    location: str
    street: str
    house_number: str
    apartment_number: str
    postal_code: str
    post_office: str
    phone: str
    email: str
    governing_body_type: str
    audience: str
    student_category: str
    school_specificity: str
    institution_type: str


@define
class ComputerPurpose(DTO):
    """The purpose of computer.

    The following information is available:
        * school_number - number of the institution in the Register of Schools and Educational Institutions
        * school_type - e.g. junior high school, adult education center, boarding school
        * school_name - full name, e.g. Non-public Junior High School No. 1 named after Irena Sendler
        * total_teaching
        * teaching_with_internet_access
        * portable_teaching
        * total_teaching_in_library
        * teaching_with_internet_access_in_library
        * teaching_portable_in_library
        * total_teaching_available_for_students
        * teaching_with_internet_access_available_for_studens
        * teaching_portable_available_for_students
        * other_total
        * other_with_internet_access
        * other_portable
        * province
        * county
        * municipality
        * location
        * street
        * house_number
        * apartment_number
        * postal_code
        * post_office
        * phone
        * email
        * governing_body_type - municipality, city with county rights, foundation, association, physical person, non-public higher education institution, commercial company, religious organization,
        * audience - public/non-public
        * student_category - children or youth, adults, without category
        * school_specificity - special/no specificity
        * institution_type - independent/composite unit
    """

    school_number: str
    school_type: str
    school_name: str
    total_teaching: [int, None]
    teaching_with_internet_access: [int, None]
    portable_teaching: [int, None]
    total_teaching_in_library: [int, None]
    total_with_internet_access_in_library: [int, None]
    teaching_portable_in_library: [int, None]
    total_teaching_available_for_students: [int, None]
    total_with_internet_access_available_for_students: [int, None]
    teaching_portable_available_for_students: [int, None]
    other_total: [int, None]
    other_with_internet_access: [int, None]
    other_portable: [int, None]
    province: str
    county: str
    munincipality: str
    location: str
    street: str
    house_number: str
    apartment_number: str
    postal_code: str
    post_office: str
    phone: str
    email: str
    governing_body_type: str
    audience: str
    student_category: str
    school_specificity: str
    institution_type: str
