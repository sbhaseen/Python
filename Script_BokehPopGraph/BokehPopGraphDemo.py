# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 16:13:58 2018

To run locally use the following method:
1. Start a python command prompt/terminal and navigate to the working directory
2. Type: bokeh serve BokehPopGraphDemo.py
3. In a browser, navigate to: http://localhost:5006/BokehPopGraphDemo

@author: shan
"""

import pandas as pd
from bokeh.plotting import Figure
from bokeh.io import curdoc
from bokeh.layouts import widgetbox, row
from bokeh.models import (HoverTool, ColumnDataSource,
                          CategoricalColorMapper, Slider, Select)
from bokeh.palettes import Spectral6

# Read in csv as a Data Frame
data = pd.read_csv('datasets/gapminder_tidy.csv', index_col='Year')

# Make the Column Data Source
source = ColumnDataSource(data={
    'x':       data.loc[1970].fertility,
    'y':       data.loc[1970].life,
    'country': data.loc[1970].Country,
    'pop':     (data.loc[1970].population / 20000000) + 2,
    'region':  data.loc[1970].region,
})

# Save the minimum and maximum values of the axes
xmin, xmax = min(data.fertility), max(data.fertility)
ymin, ymax = min(data.life), max(data.life)

# Create the figure: plot
plot = Figure(title='Gapminder Data for 1970', plot_height=400, plot_width=700,
              x_range=(xmin, xmax), y_range=(ymin, ymax))

# Set axes labels
plot.xaxis.axis_label = 'Fertility (children per woman)'
plot.yaxis.axis_label = 'Life Expectancy (years)'

# Make a list of the unique values from the region column: regions_list
regions_list = data.region.unique().tolist()

# Make a color mapper: color_mapper
color_mapper = CategoricalColorMapper(factors=regions_list, palette=Spectral6)

# Add circle glyph with a color mapper
plot.circle(x='x', y='y', fill_alpha=0.8, source=source,
            color=dict(field='region', transform=color_mapper),
            legend='region')

# Set the legend.location attribute of the plot to 'top_right'
plot.legend.location = 'top_right'

# Create a HoverTool: hover
hover = HoverTool(tooltips=[('Country', '@country')])

# Add the HoverTool to the plot
plot.add_tools(hover)


# Define the callback function
def callback(attr, old, new):
    # Read the current value off the slider and 2 dropdowns: yr, x, y
    yr = slider.value
    x = x_select.value
    y = y_select.value
    # Label axes of plot
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    # Set new_data
    new_data = {
        'x':            data.loc[yr][x],
        'y':            data.loc[yr][y],
        'country':      data.loc[yr].Country,
        'pop':          (data.loc[yr].population / 20000000) + 2,
        'region':       data.loc[yr].region,
    }
    # Assign new_data to source.data
    source.data = new_data

    # Set the range of all axes
    plot.x_range.start = min(data[x])
    plot.x_range.end = max(data[x])
    plot.y_range.start = min(data[y])
    plot.y_range.end = max(data[y])

    # Add updating title to plot
    plot.title.text = 'Gapminder data for %d' % yr


# Create widgets
slider = Slider(start=1970, end=2010, step=1, value=1970, title='Year')

x_select = Select(
    options=['fertility', 'life', 'child_mortality', 'gdp'],
    value='fertility',
    title='x-axis data')

y_select = Select(
    options=['fertility', 'life', 'child_mortality', 'gdp'],
    value='life',
    title='y-axis data')

# Attach callbacks to widgets
slider.on_change('value', callback)
x_select.on_change('value', callback)
y_select.on_change('value', callback)

# Create layout and add to current document
layout = row(widgetbox(slider, x_select, y_select), plot)
curdoc().add_root(layout)
