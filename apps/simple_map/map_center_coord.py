# -*- coding: utf-8 -*-

from branca.element import MacroElement
from jinja2 import Template

from folium.elements import JSCSSMixin
from folium.utilities import parse_options

class MapCenterCoord(JSCSSMixin, MacroElement):

    _template = Template("""
        {% macro script(this, kwargs) %}
            L.control.mapCenterCoord(
                {{ this.options|tojson }}
            ).addTo({{ this._parent.get_name() }});
        {% endmacro %}
    """)

    default_js = [
        ('MapCenterCoord_js',
         'L.Control.MapCenterCoord.js')
    ]
    default_css = [
        ('MapCenterCoord_css',
         'L.Control.MapCenterCoord.css')
    ]

    def __init__(
        self,
        position = 'bottomleft',
        icon = True,
        onMove = False,
        template = '{y} | {x}',
        projected = False,
        formatProjected = '#.##0,000',
        latlngFormat = 'DD',
        latlngDesignators = False,
        latLngFormatter = None
    ):
        super().__init__()
        self._name = 'MapCenterCoord'
        self.options = parse_options(
            position = position,
            icon = icon,
            onMove = onMove,
            template = template,
            projected = projected,
            formatProjected = formatProjected,
            latlngFormat = latlngFormat,
            latlngDesignators = latlngDesignators,
            latLngFormatter = latLngFormatter
        )
