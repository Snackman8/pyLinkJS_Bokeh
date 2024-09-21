import pandas as pd
from pylinkjs.PyLinkJS import run_pylinkjs_app
from pyLinkJS_Bokeh.bokehPlugin import pluginBokeh, obj

import json

def ready(jsc, *args):
    """ called when the webpage is loaded and ready """
    # setup raw data
    data = {'factors': ['A', 'B'],
            'x': ['A', 'B'],
            'y': [35, 45]}

    # get the chart and add some circles, stars, bars, and lines
    bc = jsc.get_bokeh_chart('chart_blank')
    bc.exec_js(f"x_range.factors = {data['factors']}")
    bc.exec_js(f"select(Bokeh.HoverTool)[0].tooltips = [['X', '@x'], ['Y', '@y']]")
    bc.column_data_source(cds_name='cds', cds_data_json=json.dumps(data))
    bc.vbar(source=obj('cds'), x=obj({'field': 'x'}), top=obj({'field': 'y'}), width=0.25)


# start the app with the Bokeh plugin
bokeh_plugin = pluginBokeh()
run_pylinkjs_app(default_html='blank_categorical_chart.html', port=8300, plugins=[bokeh_plugin])
