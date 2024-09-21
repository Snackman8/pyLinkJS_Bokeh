""" Plugin for Bokeh Applications """

# --------------------------------------------------
#    Imports
# --------------------------------------------------
import inspect
import logging
import time
import pandas as pd
import bokeh.models
import bokeh.plotting
from .bokehPlugin_util import promote_kwargs_prefix, configure_color_palette, post_process_figure
from .bokehPlugin_blank_chart import create_chart_js as create_blank_chart_js
from .bokehPlugin_blank_chart import update_chart_js as update_blank_chart_js
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
class obj:
    def __init__(self, s):
        self._s = s

    def __str__(self):
        return str(self._s)


class bokehChart:
    def __init__(self, jsc, chart_name):
        self._chart_name = chart_name
        self._jsc = jsc

        js = f"""var index=-1; for (var i=0; i<Bokeh.documents.length;i++) {{if (Bokeh.documents[i].get_model_by_name('{chart_name}')) {{index=i;}};}}; index"""
        self._doc_index = jsc.eval_js_code(js)
        if self._doc_index == -1:
            raise Exception('Chart not found in Bokeh Documents')

        self._js_chart = f"""Bokeh.documents[{self._doc_index}].get_model_by_name('{self._chart_name}')"""
        self._palette = ['#006ddb', '#db6d00', '#22cf22', '#920000', '#490092',
                         '#8f4e00', '#ff6db6', '#676767', '#004949', '#009999']
        self._color_index = {}
        self._hold = False
        self._js = ''

    def _dict_to_js_map(self, d):
        s = []
        for k, v in d.items():
            value = v
            if isinstance(value, str):
                value = f"""'{value}'"""

            s.append(f"""{k}: {value}""")
        s = ', '.join(s)
        return s

    def _add_figure_object(self, obj_type, **kwargs):
        """ add a generic bokeh glyph """
        # handle colors
        ci = self._color_index.get(obj_type, -1)
        ci = ci + 1
        self._color_index[obj_type] = ci
        if 'color' not in kwargs:
            palette = kwargs.get('palette', self._palette)
            kwargs['color'] = palette[ci % len(palette)]

        # defaults
        kwargs['name'] = kwargs.get('name', f"""{obj_type}_{ci}""")
        kwargs['legend_label'] = kwargs.get('legend_label', f"""{obj_type}_{ci}""")
        legend_label = kwargs.pop('legend_label')

        s = self._dict_to_js_map(kwargs)
        js = f"""
            {self._js_chart}.{obj_type}({{{s}}});\n"""

        if legend_label is not None:
            js += f"""
                var lio = new Bokeh.LegendItem({{label: '{legend_label}'}});
                lio.renderers.push(Bokeh.documents[{self._doc_index}].get_model_by_name('{kwargs['name']}'));
                {self._js_chart}.legend.items.push(lio);
                {self._js_chart}.change.emit();
                {self._js_chart}.legend.change.emit();
            """

        self._js += js
        if not self._hold:
            self._jsc.eval_js_code(self._js, blocking=False)
            self._js = ''

    def exec_js(self, js, global_scope=False):
        if not global_scope:
            self._js += self._js_chart + '.' + js + ';\n'
        else:
            self._js += js + ';\n'

        if not self._hold:
            self._jsc.eval_js_code(self._js, blocking=False)
            self._js = ''

    def annotate_box(self, **kwargs):
        self.exec_js(f'add_layout(new Bokeh.BoxAnnotation({{{self._dict_to_js_map(kwargs)}}}))')

    def annotate_label(self, **kwargs):
        if 'x_date_offset' in kwargs:
            # x_date_offset should be a timedelta
            td = kwargs.pop('x_date_offset')
            kwargs['x'] = kwargs['x'] + td.total_seconds() * 1000
        self.exec_js(f'add_layout(new Bokeh.Label({{{self._dict_to_js_map(kwargs)}}}))')

    def column_data_source(self, cds_name, cds_data_json):
        js = f"""{cds_name} = new Bokeh.ColumnDataSource({{'data': JSON.parse('{cds_data_json}')}}); 0;\n"""
        self.exec_js(js, global_scope=True)

    def hold(self):
        self._hold = True

    def unhold(self):
        self._hold = False
        if self._js != '':
            print(self._js)
            self._jsc.eval_js_code(self._js, blocking=False)
            self._js = ''

    def js_chart_accessor(self):
        return self._js_chart

    def annular_wedge(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def annulus(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def arc(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def asterisk(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def bezier(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def circle(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def circle_cross(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def circle_dot(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def circle_x(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def circle_y(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def cross(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def dash(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def diamond(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def diamond_cross(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def diamond_dot(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def dot(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def ellipse(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def harea(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def harea_step(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def hbar(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def hex(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def hex_tile(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def hstrip(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def hspan(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def image(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def image_rgba(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def image_url(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def inverted_triangle(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def line(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def multi_line(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def multi_polygons(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def patch(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def patches(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def plus(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def quad(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def quadratic(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def ray(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def rect(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def segment(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def square(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def square_cross(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def square_dot(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def square_pin(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def square_x(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def star(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def star_dot(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def step(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def text(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def triangle(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def triangle_dot(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def triangle_pin(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def varea(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def varea_step(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def vbar(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def vstrip(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def vspan(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def wedge(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def x(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)
    def y(self, **kwargs): self._add_figure_object(inspect.currentframe().f_code.co_name, **kwargs)


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
        self.jsc_exposed_funcs = {'add_custom_chart_type': self.add_custom_chart_type,
                                  'get_bokeh_chart': self.get_bokeh_chart,
                                  'update_chart': self._update_chart}

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
    def get_bokeh_chart(cls, jsc, chart_name) -> bokehChart:
        return bokehChart(jsc, chart_name)

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
