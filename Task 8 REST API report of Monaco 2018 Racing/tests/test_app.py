import pytest
from myapp import *
import xml.etree.ElementTree as ET

app.testing = True


@pytest.fixture()
def client():
    return app.test_client()


def test_build_api_common_statistic_json(client):
    response = client.get("/api/v1.0/report", query_string={"format": "json"})

    assert response.status_code == 200
    assert "application/json" == response.headers["Content-Type"]
    assert b'"total": 19' in response.data
    assert b'"title": "Monaco Racing 2018"' in response.data

    assert response.json["drivers"][1] == {
        "id": "EOF",
        "name": "Esteban Ocon",
        "car": "FORCE INDIA MERCEDES",
        "start_time": "12:17:58.810",
        "end_time": "1:12:11.838",
        "delta_time": "0:54:13.028000"
    }


def test_build_api_common_statistic_xml(client):
    response = client.get("/api/v1.0/report", query_string={"format": "xml"})

    root = ET.fromstring(response.data)

    for driver in root.findall("driver"):
        id = driver.findtext("id")
        name = driver.findtext("name")
        car = driver.findtext("car")
        start_time = driver.findtext("start_time")
        end_time = driver.findtext("end_time")
        delta_time = driver.findtext("delta_time")

        assert id == "LHM"
        assert name != "Stoffel Vandoorne"
        assert car == "MERCEDES"
        assert start_time == "12:18:20.125"
        assert end_time == "1:11:32.585"
        assert delta_time == "0:53:12.460000"

    assert response.status_code == 200
    assert "application/xml" == response.headers["Content-Type"]


def test_build_api_common_statistic_error(client):
    response = client.get("/api/v1.0/report", query_string={"format": ""})

    assert response.status_code == 404


def test_build_api_ordered_common_statistic_json(client):
    response = client.get("/api/v1.0/report/", query_string={"order": "asc", "format": "json"})

    assert response.status_code == 200
    assert "application/json" == response.headers["Content-Type"]
    assert b'"total": 19' in response.data
    assert b'"title": "Monaco Racing 2018"' in response.data

    assert response.json["drivers"][0] == {
        "id": "LHM",
        "name": "Lewis Hamilton",
        "car": "MERCEDES",
        "start_time": "12:18:20.125",
        "end_time": "1:11:32.585",
        "delta_time": "0:53:12.460000"
    }


def test_build_api_ordered_common_statistic_xml(client):
    response = client.get("/api/v1.0/report/", query_string={"order": "desc", "format": "xml"})

    root = ET.fromstring(response.data)

    for driver in root.findall("driver"):
        id = driver.findtext("id")
        name = driver.findtext("name")
        car = driver.findtext("car")
        start_time = driver.findtext("start_time")
        end_time = driver.findtext("end_time")
        delta_time = driver.findtext("delta_time")

        assert id == "KMH"
        assert name == "Kevin Magnussen"
        assert car == "HAAS FERRARI"
        assert start_time != "12:18:20.125"
        assert end_time == "1:04:04.396"
        assert delta_time == "1:01:13.393000"

    assert response.status_code == 200
    assert "application/xml" == response.headers["Content-Type"]


def test_build_api_ordered_common_statistic_error(client):
    response = client.get("/api/v1.0/report/", query_string={"order": "desc", "format": ""})

    assert response.status_code == 404


def test_build_api_drivers_names_json(client):
    response = client.get("/api/v1.0/report/drivers", query_string={"format": "json"})

    assert response.status_code == 200
    assert "application/json" == response.headers["Content-Type"]
    assert b'"total": 19' in response.data
    assert b'"title": "Monaco Racing 2018 Drivers"' in response.data

    assert response.json["drivers"][2] == {
        "id": "SSW",
        "name": "Sergey Sirotkin"
    }


def test_build_api_drivers_names_xml(client):
    response = client.get("/api/v1.0/report/drivers", query_string={"format": "xml"})

    root = ET.fromstring(response.data)

    for driver in root.findall("driver"):
        id = driver.findtext("id")
        name = driver.findtext("name")

        assert id == "LHM"
        assert name != "Esteban Ocon"

    assert response.status_code == 200
    assert "application/xml" == response.headers["Content-Type"]


def test_build_api_drivers_names_error(client):
    response = client.get("/api/v1.0/report/drivers", query_string={"format": ""})

    assert response.status_code == 404


def test_build_api_ordered_drivers_names_json(client):
    response = client.get("/api/v1.0/report/drivers/ordered", query_string={"order": "desc", "format": "json"})

    assert response.status_code == 200
    assert "application/json" == response.headers["Content-Type"]
    assert b'"total": 19' in response.data
    assert b'"title": "Monaco Racing 2018 Drivers"' in response.data

    assert response.json["drivers"][0] == {
        "id": "KMH",
        "name": "Kevin Magnussen"
    }


def test_build_api_ordered_drivers_names_xml(client):
    response = client.get("/api/v1.0/report/drivers/ordered", query_string={"order": "asc", "format": "xml"})

    root = ET.fromstring(response.data)

    for driver in root.findall("driver"):
        id = driver.findtext("id")
        name = driver.findtext("name")

        assert id == "LHM"
        assert name == "Lewis Hamilton"

    assert response.status_code == 200
    assert "application/xml" == response.headers["Content-Type"]


def test_build_api_ordered_drivers_names_error(client):
    response = client.get("/api/v1.0/report/drivers/ordered", query_string={"order": "asc", "format": ""})

    assert response.status_code == 404


def test_build_api_driver_json(client):
    response = client.get("/api/v1.0/report/drivers/driver", query_string={"driver_id": "SVF", "format": "json"})

    assert response.status_code == 200
    assert "application/json" == response.headers["Content-Type"]
    assert b'"title": "Monaco Racing 2018 Driver Information"' in response.data

    assert response.json["drivers"][0] == {
        "id": "SVF",
        "name": "Sebastian Vettel",
        "car": "FERRARI",
        "start_time": "12:02:58.917",
        "end_time": "1:04:03.332",
        "delta_time": "1:01:04.415000"
    }


def test_build_api_driver_xml(client):
    response = client.get("/api/v1.0/report/drivers/driver", query_string={"driver_id": "VBM", "format": "xml"})

    root = ET.fromstring(response.data)

    for driver in root.findall("driver"):
        id = driver.findtext("id")
        name = driver.findtext("name")
        car = driver.findtext("car")
        start_time = driver.findtext("start_time")
        end_time = driver.findtext("end_time")
        delta_time = driver.findtext("delta_time")

        assert id == "VBM"
        assert name == "Valtteri Bottas"
        assert car == "MERCEDES"
        assert start_time == "12:00:00.000"
        assert end_time == "1:01:12.434"
        assert delta_time == "1:01:12.434000"

    assert response.status_code == 200
    assert "application/xml" == response.headers["Content-Type"]


def test_build_api_driver_error(client):
    response = client.get("/api/v1.0/report/drivers/driver", query_string={"driver_id": "SVF", "format": ""})

    assert response.status_code == 404



