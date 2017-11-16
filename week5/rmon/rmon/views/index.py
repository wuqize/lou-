# coding=utf-8

""" rmon.views.index
the index page 's view
"""

from flask import render_template
from flask.views import MethodView


class IndexView(MethodView):
    """the index page 's view"""

    def get(self):
        """ render template
        """
        return render_template("index.html")
