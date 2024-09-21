from pylinkjs.PyLinkJS import run_pylinkjs_app
from pyLinkJS_Bokeh.bokehPlugin import pluginBokeh

def ready(jsc, *args):
    """ called when the webpage is loaded and ready """
    # get the chart and add some circles, stars, bars, and lines
    bc = jsc.get_bokeh_chart('chart_blank')
    bc.circle(x=[0,1,2,3], y=[68, 51, 97, 63], legend_label='A')
    bc.star(x=[0,1,2,3], y=[28, 91, 66, 11], legend_label=None)
    bc.vbar(x=[1.5, 2.5], top=[35, 45], width=0.25, color='purple', legend_label='BAR')
    bc.line(x=[0,1,2,3], y=[68, 51, 97, 63], legend_label='A')
    bc.line(x=[0,1,2,3], y=[28, 91, 66, 11], legend_label='B')
    bc.line(x=[0,1,2,3], y=[20, 74, 29, 88], legend_label='C')


# start the app with the Bokeh plugin
bokeh_plugin = pluginBokeh()
run_pylinkjs_app(default_html='blank_chart.html', port=8300, plugins=[bokeh_plugin])
