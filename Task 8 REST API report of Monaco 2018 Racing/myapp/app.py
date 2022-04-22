from flask import Flask, request, make_response
from flask_restful import Resource, Api, abort
import json
from dicttoxml import dicttoxml
from .report import *
import pathlib
import itertools
from flasgger import Swagger, swag_from


BASE_DIR = pathlib.Path(__file__).resolve().parent
START_DATA_FILE = BASE_DIR / 'data' / 'start.log'
FINISH_DATA_FILE = BASE_DIR / 'data' / 'end.log'
ABBREVIATIONS_FILE = BASE_DIR / 'data' / 'abbreviations.txt'

app = Flask(__name__)

template = {
    "swagger": "2.0",
    "info": {
        "title": "Flask Restful Swagger",
        "version": "0.0.1",
        "license": {
            "name": "Apache License 2.0"
        }
    }
}

app.config["SWAGGER"] = {
    "title": "Monaco Formula-1 Racing 2018 API",
    "uiversion": 3,
    "doc_dir": "/task_8_project/"
}

swag = Swagger(app, template=template)
api = Api(app)


def converter(o):
    if isinstance(o, datetime.timedelta):
        return o.__str__()


class CommonStatistic(Resource):
    def build_api_common_statistic(self):
        report = ordering(order="asc", driver_id="")
        report_converted = json.loads(json.dumps(report, default=converter))

        return {"total": len(report), "title": "Monaco Racing 2018", "drivers": report_converted}

    @swag_from("index.yml")
    def get(self):
        report_format = request.args.get("format")
        if report_format == "json":
            return self.build_api_common_statistic()
        elif report_format == "xml":
            report = self.build_api_common_statistic()
            drivers_item_func = lambda x: "driver"
            xml = dicttoxml(report, attr_type=False, custom_root="full_report", item_func=drivers_item_func)
            response = make_response(xml)
            response.headers["Content-Type"] = "application/xml"
            return response
        else:
            abort(404)


class OrderedCommonStatistic(Resource):
    def build_api_ordered_common_statistic(self):
        order = request.args.get("order")
        report = ordering(order=order, driver_id="")
        report_converted = json.loads(json.dumps(report, default=converter))

        return {"total": len(report), "title": "Monaco Racing 2018", "drivers": report_converted}

    @swag_from("index.yml")
    def get(self):
        report_format = request.args.get("format")
        if report_format == "json":
            return self.build_api_ordered_common_statistic()
        elif report_format == "xml":
            report = self.build_api_ordered_common_statistic()
            drivers_item_func = lambda x: "driver"
            xml = dicttoxml(report, attr_type=False, custom_root="full_report", item_func=drivers_item_func)
            response = make_response(xml)
            response.headers["Content-Type"] = "application/xml"
            return response
        else:
            abort(404)


class DriversNames(Resource):
    def build_api_drivers_names(self):
        drivers = ordering(order="asc", driver_id="")
        data = []
        for driver in drivers:
            driver_shorten = dict(itertools.islice(driver.items(), 2))
            driver_converted = json.loads(json.dumps(driver_shorten))
            data.append(driver_converted)

        return {"total": len(data), "title": "Monaco Racing 2018 Drivers",
                "drivers": data}

    @swag_from("index.yml")
    def get(self):
        report_format = request.args.get("format")
        if report_format == "json":
            return self.build_api_drivers_names()
        elif report_format == "xml":
            drivers = self.build_api_drivers_names()
            drivers_item_func = lambda x: "driver"
            xml = dicttoxml(drivers, attr_type=False, custom_root="short_report", item_func=drivers_item_func)
            response = make_response(xml)
            response.headers["Content-Type"] = "application/xml"
            return response
        else:
            abort(404)


class OrderedDriversNames(Resource):
    def build_api_ordered_drivers_names(self):
        order = request.args.get("order")
        drivers = ordering(order=order, driver_id="")
        data = []
        for driver in drivers:
            driver_shorten = dict(itertools.islice(driver.items(), 2))
            driver_converted = json.loads(json.dumps(driver_shorten))
            data.append(driver_converted)

        return {"total": len(data), "title": "Monaco Racing 2018 Drivers",
                "drivers": data}

    @swag_from("index.yml")
    def get(self):
        report_format = request.args.get("format")
        if report_format == "json":
            return self.build_api_ordered_drivers_names()
        elif report_format == "xml":
            drivers = self.build_api_ordered_drivers_names()
            drivers_item_func = lambda x: "driver"
            xml = dicttoxml(drivers, attr_type=False, custom_root="short_report", item_func=drivers_item_func)
            response = make_response(xml)
            response.headers["Content-Type"] = "application/xml"
            return response
        else:
            abort(404)


class Driver(Resource):
    def build_api_driver(self):
        driver_id = request.args.get("driver_id")
        driver = ordering(driver_id=driver_id, order="")
        driver_converted = json.loads(json.dumps(driver, default=converter))

        return {"title": "Monaco Racing 2018 Driver Information", "drivers": driver_converted}

    @swag_from("index.yml")
    def get(self):
        report_format = request.args.get("format")
        if report_format == "json":
            return self.build_api_driver()
        elif report_format == "xml":
            driver = self.build_api_driver()
            drivers_item_func = lambda x: "driver"
            xml = dicttoxml(driver, attr_type=False, custom_root="single_driver", item_func=drivers_item_func)
            response = make_response(xml)
            response.headers["Content-Type"] = "application/xml"
            return response
        else:
            abort(404)


api.add_resource(CommonStatistic, "/api/v1.0/report")
api.add_resource(OrderedCommonStatistic, "/api/v1.0/report/")
api.add_resource(DriversNames, "/api/v1.0/report/drivers")
api.add_resource(OrderedDriversNames, "/api/v1.0/report/drivers/ordered")
api.add_resource(Driver, "/api/v1.0/report/drivers/driver")


