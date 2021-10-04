# -*- coding: utf-8 -*-

# Run this app with `python app3.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# documentation at https://dash.plotly.com/

from flask import Flask
from os import environ

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import plotly.express as px
import plotly.graph_objects as go

import numpy as np
from numpy import random

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = Flask(__name__)
app = dash.Dash(
    server=server,
    url_base_pathname=environ.get('JUPYTERHUB_SERVICE_PREFIX', '/'),
    external_stylesheets=external_stylesheets
)

#load introduction text
intro = open('introduction.md', 'r')
intro_md = intro.read()

xmin = -300
xmax = 500
ymin = -300
ymax = 300

app.layout = html.Div([
    html.Div([
      dcc.Markdown(
        children=intro_md
      ),
    ]),

    html.Div([
        dcc.Markdown('''
          **Mohr's circle parameters**
          '''),

        html.Label('Mean stress:'),
        dcc.Slider(id='s_m', min=0, max=xmax, value=xmax/2, step=20,
            marks={0:'0', 100:'100', 200:'200', 300:'300', 400:'400', 500:'500'}
            # tooltip={'always_visible':True, 'placement':'topLeft'}
        ),

        html.Label('deviatoric stress'),
        dcc.Slider(id='s_d', min=0.0, max=150, value=80, step=10,
            marks={0:'0', 25:'25', 50:'50', 75:'75', 100:'100', 125:'125', 150:'150'}
            # tooltip={'always_visible':True, 'placement':'topLeft'}
        ),

        html.Label('theta (degrees)'),
        dcc.Slider(id='theta', min=0, max=np.pi/2, value=np.pi/4, step=np.pi/24,
            marks={0:'0', np.pi/8:'22.5', np.pi/4:'45', 3*np.pi/8:'66.5', np.pi/2:'90'},
            #tooltip={'always_visible':True, 'placement':'topLeft'}
        ),

        dcc.Checklist(
            id='circle_checkbox',
            options=[
                {'label': 'Show Mohrs Circle', 'value': 'circle'}
            ],
            value=['circle']
        )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Markdown('''
            **Failure envelope parameters**
            '''),
            html.Label('coh_stren'),
            dcc.Slider(id='s_o', min=0.0, max=150.0, value=50.0, step=10.0,
                marks={0:'0', 25:'25', 50:'50', 75:'75', 100:'100', 125:'125', 150:'150'}
            ),
            html.Label('coeff. int. frict'),
            dcc.Slider(id='mu', min=0.0, max=2.0, value=0.5, step=0.1,
                marks={0:'0', 0.5:'0.5', 1:'1', 1.5:'1.5', 2:'2'}
            ),
            dcc.Checklist(
                id='coulomb_checkbox',
                options=[
                    {'label': 'Show failure envelope', 'value': 'coulomb'},
                ],
                value=['coulomb']
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='mean_dev_graph'),
        ]),

    html.Div([
       dcc.Markdown('''
           ----

           ### Sources
           ''')
     ])
],style={'width': '800px'})




# The callback function with it's app.callback wrapper.
@app.callback(
    Output('mean_dev_graph', 'figure'),
    Input('circle_checkbox', 'value'),
    Input('coulomb_checkbox', 'value'),
    Input('s_m', 'value'),
    Input('s_d', 'value'),
    Input('theta', 'value'),
    Input('s_o', 'value'),
    Input('mu', 'value')
    )
def update_graph(circle_checkbox, coulomb_checkbox, s_m, s_d, theta, s_o, mu,):
# array for drawing a circle, angle going from 0 to 90 since 2*angle is used.
# for a whole circle, use np.pi, not np.pi/2

    angle = np.linspace(0, np.pi, 100)

# build the mohr's circle and coulomb failure line
    s3 = s_m - s_d
    s1 = s_m + s_d

    coulx1 = np.linspace(0, xmax, 50)
    couly1 = s_o + mu*coulx1
    coulx2 = np.linspace(0, xmax, 50)
    couly2 = -s_o - mu*coulx2

    s_n = 0.5*(s1 + s3) + 0.5*(s1 - s3)*np.cos(2*angle)
    s_s = 0.5*(s1 - s3)*np.sin(2*angle)

# draw the angle representing the plane of interest
    x = np.array([s_m, 0.5*(s1 + s3) + 0.5*(s1 - s3)*np.cos(2*theta)])
    y = np.array([0, 0.5*(s1 - s3)*np.sin(2*theta)])

    # generate the plot.
    fig = go.Figure()

    if circle_checkbox == ['circle']:
       fig.add_trace(go.Scatter(x=s_n, y=s_s, mode='lines', name='circle'))
       fig.add_trace(go.Scatter(x=x, y=y, name="linear", line_shape='linear', line=dict(color='green')))

    if coulomb_checkbox == ['coulomb']:
       fig.add_trace(go.Scatter(x=coulx1, y=couly1, mode='lines', name='Coulomb+', line=dict(color='red')))
       fig.add_trace(go.Scatter(x=coulx2, y=couly2, mode='lines', name='Coulomb-', line=dict(color='red')))

    # We want a "square" figure so the circle is seen as a circle
    # Ranges for xaxis and yaxis, and the plot width/height must be be chosen for a square graph. 
    # width and height are in pixels.
    fig.update_layout(xaxis_title='Sigma_n', yaxis_title='Sigma_s', width=600, height=500, showlegend=False)
#    fig.update_layout(xaxis_title='Sigma_n', yaxis_title='Sigma_s', width=800, height=660, showlegend=False)
    fig.update_xaxes(range=[xmin, xmax])
    fig.update_yaxes(range=[ymin, ymax])
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
