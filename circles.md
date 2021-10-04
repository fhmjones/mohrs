---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.4
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Mohr circle plotting

First attempts to draw a Mohr's circle given $\sigma_1$ and $\sigma_3$. Initial reference is PDF file "MohrCircle details.pdf", in this repository. 

For more comprehensive geological context try Ch. 6 of Allmendinger, at Cornell, in PDF [here](http://www.geo.cornell.edu/geology/faculty/RWA/structure-lab-manual/chapter-6.pdf).

```python
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
```

```python
# array for angle theta 
# Theta is the angle between vertical and the normal to the plan of interest. 
# It goes from 0 to 90 degrees, meaning horizontal to vertical
# theta = np.linspace(0, np.pi/2, 100)

# for a whole circle, use np.pi, not np.pi/2
# BUT - graph axes and plot shape will need adjusting
theta = np.linspace(0, np.pi, 100)

# s_m = mean_stress 
# s_d = deviatoric_stress 
# s_1 = the maximum stress, or long axis of the stress ellipse.
# s_3 = stress perpendicular to s_1, or the short axis of the stress ellipse.

s_m = 0.7
s_d = 0.5
s3 = s_m - s_d
s1 = s_m + s_d

# xmax = x axis max
# ymax - y axis max
xmax = 3.0
ymax = 1.5

# for Coloumb failure line: 
# s_o is cohesive strength (yaxis crossing)
# mu is slope, which is coefficient of internal friction (delta s_n / delta s_s)
s_o = 0.3
mu = 0.4
coulx1 = np.linspace(0, xmax, 50)
couly1 = s_o + mu*coulx1
coulx2 = np.linspace(0, xmax, 50)
couly2 = -s_o - mu*coulx2
```

```python
# equation for drawing a circle as normal and shear stresses vary
# These are normal and shear stresses on a plane as that plane varies between 
#   vertical (parallel to s_1's direction) and horizontal (perpendicular)

s_n = 0.5*(s1 + s3) + 0.5*(s1 - s3)*np.cos(2*theta)
s_s = 0.5*(s1 - s3)*np.sin(2*theta)

# generate the plot.
fig = go.Figure()
fig.add_trace(go.Scatter(x=s_n, y=s_s,
               mode='lines',
               name='circle'))
fig.add_trace(go.Scatter(x=coulx1, y=couly1,
               mode='lines',
               name='Coulomb+',
               line=dict(color='red')))
fig.add_trace(go.Scatter(x=coulx2, y=couly2,
               mode='lines',
               name='Coulomb-',
               line=dict(color='red')))

# We want a "square" figure so the circle is seen as a circle
# Ranges for xaxis and yaxis, and the plot width/height must be be chosen for a square graph. 
# width and height are in pixels.
fig.update_layout(xaxis_title='Sigma_n', yaxis_title='Sigma_s', width=600, height=500, showlegend=False)
fig.update_xaxes(range=[-1, xmax])
fig.update_yaxes(range=[-1.5, ymax])

fig.show()
```

```python

```

```python

```
