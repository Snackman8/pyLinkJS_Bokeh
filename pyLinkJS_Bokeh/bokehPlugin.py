""" Plugin for Bokeh Applications """

# --------------------------------------------------
#    Imports
# --------------------------------------------------
import logging
import time
import pandas as pd
import bokeh.models
import bokeh.plotting
from .bokehPlugin_util import promote_kwargs_prefix, configure_color_palette, post_process_figure
from .bokehPlugin_boxplot_chart import create_chart_js as create_boxplot_chart_js
from .bokehPlugin_boxplot_chart import update_chart_js as update_boxplot_chart_js
from .bokehPlugin_hbar_chart import create_chart_js as create_hbar_chart_js
from .bokehPlugin_hbar_chart import update_chart_js as update_hbar_chart_js
from .bokehPlugin_line_chart import create_chart_js as create_line_chart_js
from .bokehPlugin_line_chart import update_chart_js as update_line_chart_js
from .bokehPlugin_pie_chart import create_chart_js as create_pie_chart_js
from .bokehPlugin_pie_chart import update_chart_js as update_pie_chart_js
from .bokehPlugin_vbar_chart import create_chart_js as create_vbar_chart_js
from .bokehPlugin_vbar_chart import update_chart_js as update_vbar_chart_js
from .bokehPlugin_histogram_chart import create_chart_js as create_histogram_chart_js
from .bokehPlugin_histogram_chart import update_chart_js as update_histogram_chart_js
from .bokehPlugin_table_chart import create_chart_js as create_table_chart_js
from .bokehPlugin_table_chart import update_chart_js as update_table_chart_js

# --------------------------------------------------
#    Plugin
# --------------------------------------------------
class pluginBokeh:
    """ plugin for bokeh application """
    # --------------------------------------------------
    #    Class Variables
    # --------------------------------------------------
    BOKEH_CONTEXT = {}

    # --------------------------------------------------
    #    Constructor and Plugin Registration
    # --------------------------------------------------
    def __init__(self, get_data_handler=None):
        """ init """
        self._get_data_handler = get_data_handler
        self._kwargs = {
            'global_template_vars': {'create_chart': self._create_chart}
            }
        self.jsc_exposed_funcs = {'update_chart': self._update_chart,
                                  'add_custom_chart_type': self.add_custom_chart_type}

    def inject_html_top(self):
        return """
            <head>
            <!-- bokeh -->
            <script src="https://cdn.bokeh.org/bokeh/release/bokeh-3.1.1.min.js" crossorigin="anonymous"></script>
            <script src="https://cdn.bokeh.org/bokeh/release/bokeh-widgets-3.1.1.min.js" crossorigin="anonymous"></script>
            <script src="https://cdn.bokeh.org/bokeh/release/bokeh-tables-3.1.1.min.js" crossorigin="anonymous"></script>
            <script src="https://cdn.bokeh.org/bokeh/release/bokeh-api-3.1.1.min.js" crossorigin="anonymous"></script>
            <script src="https://cdn.bokeh.org/bokeh/release/bokeh-gl-3.1.1.min.js" crossorigin="anonymous"></script>
            <script src="https://cdn.bokeh.org/bokeh/release/bokeh-mathjax-3.1.1.min.js" crossorigin="anonymous"></script>
            </head>"""


    def register(self, kwargs):
        """ callback to register this plugin with the framework """
        # merge the dictionaries
        d = kwargs.get('global_template_vars', {})
        d.update(self._kwargs['global_template_vars'])
        self._kwargs['global_template_vars'] = d
        kwargs.update(self._kwargs)

    # --------------------------------------------------
    #    Event Handlers
    # --------------------------------------------------
    # @classmethod
    # def on_context_close(cls, jsc):
    #     pass
    #
    # @classmethod
    # def on_context_open(cls, jsc):
    #     pass


    @classmethod
    def _extract_targetclass_kwargs(cls, targetclass, kwargs, delete=False):
        """ extract kwargs which match attibutes available on the target class

            Args:
                targetclass - class to check for attributes on
                kwargs - kwargs dictionary
                delete - if True, will remove matched items from kwargs

            Returns:
                dictionary of matched key values
        """
        params = {}
        for k in dir(targetclass):
            if (not k.startswith('_')) and (k in kwargs):
                params[k] = kwargs[k]
                if delete:
                    del kwargs[k]
        return params

    @classmethod
    def _prep_for_chart(cls, **kwargs):
        """ perform common preprocessing before creating a chart

            Kwargs:
                df - dataframe containing the data for the chart
#                title - title of the figure, shorthand for __figure__title
                user_palette - palette for glyphs in the chart

            Returns:
                dictionary of processed variables necessary for chart generation
                    palette - generate color palette for the chart
                    cds - ColumnDataSource for the chart
        """
        # fix kwargs
#        kwargs['title'] = kwargs.get('title', '')
        kwargs['user_palette'] = kwargs.get('user_palette', None)
        kwargs['name'] = kwargs.get('name', str(time.time()))

        # init the prepped values
        pv = {}

        # fix df
        df = kwargs.get('df', None)
        if df is None:
            df = pd.DataFrame()
        df = df.copy()

        # setup X axis index in the dataframe
        if 'X' in df.columns:
            df = df.set_index('X')
        else:
            df.index.name = 'X'
        pv['df'] = df

        # generate the palette
        pv['palette'] = configure_color_palette(pv['df'], kwargs.get('user_palette', None))

        # create the column data source for bokeh
        pv['df'].columns = pv['df'].columns.map(str)
        pv['cds'] = bokeh.models.ColumnDataSource(bokeh.models.ColumnDataSource.from_df(pv['df']))

        # save the target div
        pv['div_id'] = f"div_{kwargs['name']}"

        # compute the figure_kwargs
        figure_kwargs = cls._extract_targetclass_kwargs(bokeh.plotting.figure, kwargs, delete=True)
#        figure_kwargs.update(promote_kwargs_prefix(['__figure__'], kwargs))
        if 'x_axis_type' in kwargs:
            figure_kwargs['x_axis_type'] = kwargs['x_axis_type']
        pv['figure_kwargs'] = figure_kwargs
        pv['kwargs'] = kwargs

        # success!
        return pv


    def add_custom_chart_type(self, chart_type, create_func, update_func):
        globals()[f'create_{chart_type}_chart_js'] = create_func
        globals()[f'update_{chart_type}_chart_js'] = update_func

    def _create_chart(self, chart_type, page_instance_id, jsc_sequence_number=0, **kwargs):
        # create the document if needed
        if page_instance_id not in self.BOKEH_CONTEXT:
            self.BOKEH_CONTEXT[page_instance_id] = {}
            self.BOKEH_CONTEXT[page_instance_id]['kwargs'] = {}

        # save the chart_type and kwargs
        kwargs['chart_type'] = kwargs.get('chart_type', chart_type)
        self.BOKEH_CONTEXT[page_instance_id]['kwargs'][kwargs['name']] = kwargs
        pv = self._prep_for_chart(**kwargs)
        try:
            func_js = globals()[f'create_{chart_type}_chart_js']
            div = f"<div id={pv['div_id']} style='margin:0 px; padding: 0px; width:100%; height:100%;'></div>"
            script = f"<script>{func_js(pv)}</script>"
            return div + script
        except:
            return '<div>Unable to create chart</div>'


    @classmethod
    def _update_chart(cls, jsc, chart_name, df):
        # get the kwargs for the chart when itw as created
        if chart_name not in cls.BOKEH_CONTEXT[jsc.page_instance_id]['kwargs']:
            logging.info(f'"{chart_name}" not found on page')
            return
        kwargs = cls.BOKEH_CONTEXT[jsc.page_instance_id]['kwargs'][chart_name]

        # calcualte prepared values
        pv = cls._prep_for_chart(df=df, **kwargs)

        # call the update_js for the chart type, i.e. update_line_chart_js
        func_js = globals()[f'update_{kwargs["chart_type"]}_chart_js']
        js = func_js(pv)

        js = js + cls.BOKEH_CONTEXT[jsc.page_instance_id]['kwargs'][chart_name].get('post_figure_update_js', '')

        jsc.eval_js_code(js, blocking=False)
