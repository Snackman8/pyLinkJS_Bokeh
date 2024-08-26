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
| y_axis_label | caption for the y axis |

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


#### Box Plot Chart

 <br>
 <br>

#### Historgram Chart

 <br>
 <br>

#### Vertical Area Chart

 <br>
 <br>

#### Custom Chart
