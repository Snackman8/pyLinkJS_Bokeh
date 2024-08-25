# pyLinkJS_Bokeh
Plugin for pyLinkJs that creates charts for dashboards using the Bokeh Library

### Table of Contents
**[Installation](#installation)**<br>


## Installation

The easiest way to install is to install directly from github using pip
```
sudo pip3 install pip install git+https://github.com/Snackman8/pyLinkJS
```

Or clone this repository to your home directory and then pip3 install
```
cd ~
git clone https://github.com/Snackman8/pyLinkJS_Bokeh
cd pyLinkJS_Bokeh
sudo pip3 install .
```

## Basic Example

Create the two files below for a simple example

#### example.py
```python


import pandas as pd
from pylinkjs.PyLinkJS import run_pylinkjs_app
from pyLinkJS_Bokeh.bokehPlugin import pluginBokeh

def ready(jsc, *args):
    """ called when the webpage is loaded and ready """
    # when the page is ready, create the dataframe and refresh the chart
    data = {'A': [ 68, 51, 97, 63],
            'B': [ 28, 91, 66, 11],
            'C': [ 20, 74, 29, 88]}    
    df = pd.DataFrame(data)

    # refresh chart
    jsc.update_chart('chart_line', df)

# start the app with the Bokeh plugin
bokeh_plugin = pluginBokeh()
run_pylinkjs_app(default_html='example.html', port=8300, plugins=[bokeh_plugin])
```

#### example.html
```html
<body>
    <h1>Example Line Chart</h1>

    {% raw create_chart(name='chart_line', chart_type='line', title='Example Line chart', width=600, height=400, 
                        x_axis_label='X-Axis', y_axis_label='Y-Axis',
                        page_instance_id=page_instance_id) %}
</body>
```

## Common Parameters for Charts
| Parameter | Description |
| --- | --- |
| name | Unique name of the chart.  Used to access the chart from Python |
| chart_type | the type of chart, i.e. 'line' or 'pie' |
| title | The display title of the chart |
| width | width of the chart in pixels |
| height | height of the chart in pixels |
| x_axis_label | caption for the x axis |
| y_axis_label | caption for the y axis |
| page_instance_id | magic id for the page the chart is associated with |
| toolbar_visible | If set to False, will hide the Bokeh toolbar (Default True) |

## Line Chart

<table>
<tr><th>line_chart.py</th><th>line_chart.html</th></tr>
<tr><td><pre>
    data = {'A': [ 68, 51, 97, 63],
            'B': [ 28, 91, 66, 11],
            'C': [ 20, 74, 29, 88]}    
    df = pd.DataFrame(data)
    jsc.update_chart('chart_line', df)
</pre></td>
<td><pre>
{% raw create_chart(name='chart_line', chart_type='line',
                    page_instance_id=page_instance_id) %}
</pre></td>
<td>
![image](https://github.com/user-attachments/assets/65bdfb5e-50d1-4068-a2ca-48348fc8aeda)
</td>
</tr>
</table>
