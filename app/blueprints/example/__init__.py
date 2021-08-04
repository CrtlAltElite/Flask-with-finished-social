from flask import Blueprint

bp = Blueprint('example',__name__, url_prefix='/example')

from .import models