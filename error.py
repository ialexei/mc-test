from flask_api.exceptions import APIException


class InvalidParameter(APIException):
  status_code = 400

  def __init__(self, message):
    self.detail = message


class RecordNotFound(APIException):
  status_code = 404

  def __init__(self, message):
    self.detail = message
