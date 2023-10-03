# --------------------------------------------------
#    Imports
# --------------------------------------------------
import logging
import numpy as np
import pandas as pd
from pylinkjs.PyLinkJS import run_pylinkjs_app
from pyLinkJS_Bokeh.bokehPlugin import pluginBokeh


# --------------------------------------------------
#    Functions
# --------------------------------------------------

from pyLinkJS_Bokeh.bokehPlugin_util import post_process_figure, promote_kwargs_prefix, reset_figure


# --------------------------------------------------
#    Functions
# --------------------------------------------------
def myline_chart_create_chart_js(pv):
    """ Create the javascript to create a chart
    
        Args:
            target_div_id - id of the div which will contain the chart
            pv - dict of prepared values
                    'df' - dataframe passed in by user
                    'div_id' - id of the div to target
                    'figure_kwargs' - keyword args passed in that affect figure creation
                        'name' - name of the chart
                        (see bokeh Figure documentation for full list)
                    'kwargs' - keyword arguments passed in during initial chart creation
                        (keyword args prefaced with __wedge__ will be passed in for wedge creation.
                         see Bokeh wedge documentation for full list of available keywords)
                    'palette' - color palette to use for chart rendering

        Returns:
            javascript to create the initial chart
    """
    js = f"""
        var plt = Bokeh.Plotting;
        var f = new plt.Figure({pv['figure_kwargs']});
        """
    js += post_process_figure(**pv['kwargs'])
    js += myline_chart_update_chart_js(pv)
    js += f"""plt.show(f, '#{pv["div_id"]}');"""
    
    return js


def myline_chart_update_chart_js(pv):
    """ update the chart with new data

            Dataframe Input

                - A, B, C are the names of the lines
                - 0, 1, 2 is the X axis
                - cell values are the Y values

                    A   B   C
                0  58   5  51
                1  51  85  83
                2   5  70  95

        Args:
            pv - see create_chart_js documentation for pv documentation

        Returns:
            javascript to update the chart with new data
    """    
    # reset the figure
    js = reset_figure(pv['df'], pv['figure_kwargs']['name'])

    # add the new glyphs
    for i, c in enumerate(pv['df'].columns):
        kwd = {}
        kwd['source'] = 'cds'
        kwd['x'] = "{field: 'X'}"
        kwd['y'] = f"{{field: '{c}'}}"
        kwd['color'] = f"'{pv['palette'][i]}'"
        kwd.update(promote_kwargs_prefix(['__line__', f'__line_{i}__'], pv['kwargs']))
        kwds = ', '.join([f"'{k}': {v}" for k, v in kwd.items()])

        js += f"""
            // add the line    
            var lo = f.line({{ {kwds} }});
            
            // add the legend item
            var lio = new Bokeh.LegendItem({{label: '{c}'}});
            lio.renderers.push(lo);
            f.legend.items.push(lio);
            f.legend.change.emit();
        """
    return js





def refresh_charts(jsc, columns = 3):
    # create a random dataframe
    rows = np.random.randint(4, 10)
    column_headers = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:columns])
    df = pd.DataFrame(np.random.randint(0,100,size=(rows, columns)), columns=column_headers)

    jsc.update_chart('chart_myline', df)
    

def ready(jsc, *args):
    """ called when a webpage creates a new connection the first time on load """
    refresh_charts(jsc)


# --------------------------------------------------
#    Main
# --------------------------------------------------
def main():
    # configure logger
    logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')

    # define the port
    port = 8300

    # init the google oauth2 plugin
    bokeh_plugin = pluginBokeh()
    bokeh_plugin.add_custom_chart_type('myline', myline_chart_create_chart_js, myline_chart_update_chart_js)

    # run the application
    run_pylinkjs_app(default_html='custom_chart_type.html',
                     port=port,
                     plugins=[bokeh_plugin])

if __name__ == '__main__':
    main()
