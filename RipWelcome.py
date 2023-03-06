from http import HTTPStatus

from flask_restful import Resource


class RipWelcome(Resource):
    @staticmethod
    def get():
        return {"result": "hallo world", "request": "welcome"}, HTTPStatus.OK
