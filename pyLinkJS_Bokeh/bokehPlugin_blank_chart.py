""" functions to create a blank chart for the Bokeh PyLinkeJS plugin """

# --------------------------------------------------
#    Imports
# --------------------------------------------------
from .bokehPlugin_util import post_process_figure


# --------------------------------------------------
#    Functions
# --------------------------------------------------
def create_chart_js(pv):
    js = f"""
        var plt = Bokeh.Plotting;
        var f = new plt.Figure({pv['figure_kwargs']});
        """
    js += post_process_figure(**pv['kwargs'])
    js += update_chart_js(pv)
    js += f"""plt.show(f, '#{pv["div_id"]}');"""
    
    return js


def update_chart_js(pv):    
    return ''
