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
| page_instance_id | magic id for the page the chart is associated with |
| height | height of the chart in pixels |
| title | The display title of the chart |
| toolbar_visible | If set to False, will hide the Bokeh toolbar (Default True) |
| width | width of the chart in pixels |
| x_axis_label | caption for the x axis |
| x_axis_type | type of scale for x-axis, can be 'auto' or 'datetime' <br> for datetime, use milliseconds after epoch <br> i.e. if the index is datetime64ns, use `df.index.map(pd.Timestamp.timestamp) * 1000` |
| y_axis_label | caption for the y axis |
| y_axis_type | type of scale for y-axis, can be 'auto' or 'datetime' <br> for datetime, use milliseconds after epoch <br> i.e. if the index is datetime64ns, use `df.index.map(pd.Timestamp.timestamp) * 1000` |

## Python Methods for Charts

refresh_chart

`jsc.refresh_chart('chart_line')`

set_chart_property

`jsc.set_chart_property('chart_line', 'xaxes[0].axis_line_color', '"red"')`

update_chart

`jsc.update_chart('chart_line', df)`



## Chart Documentation

### Line Chart
<table width=100%>
<tr><th>Python</th><th>HTML</th></tr>
<tr valign=top><td><pre lang="python">
# Line Chart

data = {'A': [68, 51, 97, 63],
        'B': [28, 91, 66, 11],
        'C': [20, 74, 29, 88]}    
df = pd.DataFrame(data)
jsc.update_chart('chart_line', df)
</pre></td>
<td><pre pre lang="python">
 <br>
{% raw create_chart(name='chart_line', chart_type='line',
                    page_instance_id=page_instance_id) %}
</pre></td>
</tr>
<tr><th>DataFrame</th><th>Image</th></tr>
<tr valign=top><td><pre>
    A   B   C
0  68  28  20
1  51  91  74
2  97  66  29
3  63  11  88    
</pre></td><td><img src="https://github.com/user-attachments/assets/0a07a722-0db0-4ba9-b979-4e8b112ba68f"></td>    
</tr>
</table>

 <br>

### Pie Chart
<table width=100%>
<tr><th>Python</th><th>HTML</th></tr>
<tr valign=top><td><pre lang="python">
# Pie Chart
data = {'A': [68, 'AA'],
        'B': [28, 'BB'],
        'C': [20, 'CC']}    
df = pd.DataFrame(data, index=['value', 'text'])
jsc.update_chart('chart_pie', df)
</pre></td>
<td><pre pre lang="python">
 <br>
{% raw create_chart(name='chart_pie', chart_type='pie',
                    page_instance_id=page_instance_id) %}
</pre></td>
</tr>
<tr><th>DataFrame</th><th>Image</th></tr>
<tr valign=top><td><pre>
        A   B   C
value  68  28  20
text   AA  BB  CC
</pre></td><td><img src="https://github.com/user-attachments/assets/2329e0a3-129a-4cb8-850b-cfcb369a63a6"></td>    
</tr>
</table>

 <br>

### Horizontal Bar Chart
<table width=100%>
<tr><th>Python</th><th>HTML</th></tr>
<tr valign=top><td><pre lang="python">
# Horizontal Bar Chart
data = {'A': [68],
        'B': [28],
        'C': [20]}    
df = pd.DataFrame(data, index=['Z'])
jsc.update_chart('chart_hbar', df)
</pre></td>
<td><pre pre lang="python">
 <br>
{% raw create_chart(name='chart_hbar', chart_type='hbar',
                    page_instance_id=page_instance_id) %}
</pre></td>
</tr>
<tr><th>DataFrame</th><th>Image</th></tr>
<tr valign=top><td><pre>
    A   B   C
Z  68  28  20
<br>
<i>The index is the y-axis label for the bars</i>
</pre></td><td><img src="https://github.com/user-attachments/assets/c393e85f-14cf-4a94-b42f-05b20914e4b0"></td>
</tr>
</table>

 <br>
 <br>

#### Horizontal Bar Chart Grouped
<table width=100%>
<tr><th>Python</th><th>HTML</th></tr>
<tr valign=top><td><pre lang="python">
# Horizontal Bar Chart
data = {'A': [93, 8, 68],
        'B': [8, 21, 44],
        'C': [68, 28, 20]}    
df = pd.DataFrame(data, index=['X', 'Y', 'Z'])
jsc.update_chart('chart_hbar_grouped', df)
</pre></td>
<td><pre pre lang="python">
 <br>
{% raw create_chart(name='chart_hbar_grouped', chart_type='hbar',
                    page_instance_id=page_instance_id) %}
</pre></td>
</tr>
<tr><th>DataFrame</th><th>Image</th></tr>
<tr valign=top><td><pre>
    A   B   C
X  93  63   8
Y   8  21  44
Z  68  28  20
<br>
<i>The index is the y-axis label for the bars</i>
</pre></td><td><img src="https://github.com/user-attachments/assets/a929678c-5ef5-4cf6-b167-38160a1e9b1b"></td>
</tr>
</table>

 <br>
 <br>

### Vertical Bar Chart
<table width=100%>
<tr><th>Python</th><th>HTML</th></tr>
<tr valign=top><td><pre lang="python">
# Vertical Bar Chart
data = {'A': [68],
        'B': [28],
        'C': [20]}    
df = pd.DataFrame(data, index=['Z'])
jsc.update_chart('chart_vbar', df)
</pre></td>
<td><pre pre lang="python">
 <br>
{% raw create_chart(name='chart_vbar', chart_type='vbar',
                    page_instance_id=page_instance_id) %}
</pre></td>
</tr>
<tr><th>DataFrame</th><th>Image</th></tr>
<tr valign=top><td><pre>
    A   B   C
Z  68  28  20
<br>
<i>The index is the x-axis label for the bars</i>
</pre></td><td><img src="https://github.com/user-attachments/assets/278888cf-a841-406f-86a6-38f2712be01c"></td>
</tr>
</table>

 <br>
 <br>

#### Vertical Bar Chart Grouped
<table width=100%>
<tr><th>Python</th><th>HTML</th></tr>
<tr valign=top><td><pre lang="python">
# Vertical Bar Chart
data = {'A': [93, 8, 68],
        'B': [8, 21, 44],
        'C': [68, 28, 20]}    
df = pd.DataFrame(data, index=['X', 'Y', 'Z'])
jsc.update_chart('chart_vbar_grouped', df)
</pre></td>
<td><pre pre lang="python">
 <br>
{% raw create_chart(name='chart_vbar_grouped', chart_type='vbar',
                    page_instance_id=page_instance_id) %}
</pre></td>
</tr>
<tr><th>DataFrame</th><th>Image</th></tr>
<tr valign=top><td><pre>
    A   B   C
X  93  63   8
Y   8  21  44
Z  68  28  20
<br>
<i>The index is the x-axis label for the bars</i>
</pre></td><td><img src="https://github.com/user-attachments/assets/62158af0-b3a1-4131-b7de-210045fecacc"></td>
</tr>
</table>

 <br>
 <br>

#### Table Chart
<table width=100%>
<tr><th>Python</th><th>HTML</th></tr>
<tr valign=top><td><pre lang="python">
# Table Chart
data = {'A': [93, 8, 68],
        'B': [8, 21, 44],
        'C': [68, 28, 20]}    
df = pd.DataFrame(data)
jsc.update_chart('chart_table', df)
</pre></td>
<td><pre pre lang="python">
 <br>
{% raw create_chart(name='chart_table', chart_type='table',
                    page_instance_id=page_instance_id) %}
</pre></td>
</tr>
<tr><th>DataFrame</th><th>Image</th></tr>
<tr valign=top><td><pre>
    A   B   C
0  93  63   8
1   8  21  44
2  68  28  20
</pre></td><td><img src="https://github.com/user-attachments/assets/723a47d8-66a0-4ef8-ad0b-02f6863db009"></td>
</tr>
</table>

 <br>
 <br>

#### Histogram Chart
<table width=100%>
<tr><th>Python</th><th>HTML</th></tr>
<tr valign=top><td><pre lang="python">
# Histogram Chart
data = {'counts': [17, 96, 13, 7, 48],
        'bin_text': ['A A', 'B B', 'C C', 'D D', 'E E']}
df = pd.DataFrame(data, index=['A', 'B', 'C', 'D', 'E'])
jsc.update_chart('chart_histogram', df)
</pre></td>
<td><pre pre lang="python">
 <br>
{% raw create_chart(name='chart_histogram', chart_type='histogram',
                    page_instance_id=page_instance_id) %}
</pre></td>
</tr>
<tr><th>DataFrame</th><th>Image</th></tr>
<tr valign=top><td><pre>
   counts bin_text
A      17      A A
B      96      B B
C      13      C C
D       7      D D
E      48      E E
</pre></td><td><img src="https://github.com/user-attachments/assets/64837160-7146-40c7-af02-91fda4a11838"></td>
</tr>
</table>

 <br>
 <br>

#### Box Plot Chart

_DOCUMENTATION NOT READY YET_

 <br>
 <br>

#### Vertical Area Chart

_DOCUMENTATION NOT READY YET_

 <br>
 <br>

#### Custom Chart

_DOCUMENTATION NOT READY YET_

## Advanced Examples

#### Dates on X-Axis
<table width=100%>
<tr><th>Python</th><th>HTML</th></tr>
<tr valign=top><td><pre lang="python">
# Line chart with date on x-Axis
data = {'A': [28, 91, 66, 11]}
index = pd.to_datetime(['2024-01-01', 2024-01-02',
                        '2024-01-03', '2024-01-04'])
# convert from datetime64ns to ms after epoch format
index = index.map(pd.Timestamp.timestamp) * 1000
# create dataframe
df = pd.DataFrame(data=data, index=index)
# update chart
jsc.update_chart('chart_line', df)
</pre></td>
<td><pre pre lang="python">
 <br>
{% raw create_chart(name='chart_line', chart_type='line',
                    x_axis_type='datetime',
                    page_instance_id=page_instance_id) %}
</pre></td>
</tr>
<tr><th>DataFrame</th><th>Image</th></tr>
<tr valign=top><td><pre>
               A
1.704067e+12  28
1.704154e+12  91
1.704240e+12  66
1.704326e+12  11    
</pre></td><td><img src="https://github.com/user-attachments/assets/a3a9d83b-2793-4c71-a3cd-558c8acc8597"></td>
</tr>
</table>

 <br>
 <br>

## Advanced Blank Chart Example

Create the two files below for an advanced blank chart example

#### blank_chart.py
```python


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
```

#### blank_chart.html
```html
<body>
    {% raw create_chart(name='chart_blank', chart_type='blank', width=600, height=400, 
                        page_instance_id=page_instance_id) %}
</body>
```

## Advanced Blank Chart with Categorical Axis Example

#### blank_categorical_chart.py
```python


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
```

#### blank_categorical_chart.html
```html
<body>
    {% raw create_chart(name='chart_blank', chart_type='blank', width=600, height=400,
                        x_range = [],
                        page_instance_id=page_instance_id) %}
</body>
```

