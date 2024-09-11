from pylinkjs.PyLinkJS import run_pylinkjs_app
from pyLinkJS_Bokeh.bokehPlugin import pluginBokeh

def ready(jsc, *args):
    """ called when the webpage is loaded and ready """
    # get the chart and add some circles, stars, bars, and lines
    bc = jsc.get_bokeh_chart('chart_blank')
    bc.exec_js("x_range.factors = ['A', 'B']")    
    bc.vbar(x=['A', 'B'], top=[35, 45], width=0.25)


# start the app with the Bokeh plugin
bokeh_plugin = pluginBokeh()
run_pylinkjs_app(default_html='blank_categorical_chart.html', port=8300, plugins=[bokeh_plugin])
