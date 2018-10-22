import pandas as pd
from bokeh.io import curdoc
from bokeh.models import (ColumnDataSource, CategoricalColorMapper,
Slider, HoverTool, Select, BoxSelectTool, LassoSelectTool)
from bokeh.plotting import figure
from bokeh.palettes import Category10
from bokeh.layouts import row,widgetbox

#### DATA ####
data = pd.read_csv('gapminder.csv')
data.index = data.Year
del(data['Year'])
region_list = data.region.unique().tolist()
source = ColumnDataSource(data={
    'x':        data.loc[1970].fertility,
    'y':        data.loc[1970].life,
    'country':  data.loc[1970].Country,
    'pop':      data.loc[1970].population/1000000,
    'region':   data.loc[1970].region})

xmin, xmax = min(data.fertility), max(data.fertility)
ymin, ymax = min(data.life), max(data.life)

#### CALLBACKS ####
def update_plot(attr,old,new):
    yr = slider.value
    x = x_select.value
    y = y_select.value
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    new_data = {
    'x':        data.loc[yr][x],
    'y':        data.loc[yr][y],
    'country':  data.loc[yr].Country,
    'pop':      data.loc[yr].population/1000000,
    'region':   data.loc[yr].region}
    source.data = new_data
    plot.title.text = 'Gapminder data for %d' %yr
    plot.x_range.start = min(data[x])
    plot.x_range.end = max(data[x])
    plot.y_range.start = min(data[y])
    plot.y_range.end = max(data[y])

#### WIDGETS ####
color_mapper = CategoricalColorMapper(factors = region_list,
                                      palette=Category10[len(region_list)])
slider = Slider(title = 'Year', start = 1964, end = 2013, step = 1,value = 1970)
slider.on_change('value',update_plot)
hover = HoverTool(tooltips=[('Country', '@country'),('Population','@pop')])
box_select = BoxSelectTool()
lasso_select = LassoSelectTool()
x_select = Select(options=['fertility', 'life', 'child_mortality', 'gdp'],
                    value='fertility',
                    title='x-axis data')
x_select.on_change('value',update_plot)
y_select = Select(options=['fertility', 'life', 'child_mortality', 'gdp'],
                    value='life',
                    title='y-axis data')
y_select.on_change('value',update_plot)

#### PLOT ####
plot = figure(title='Gapminder Data for 1970',plot_height=500,plot_width=600,
              x_range=(xmin,xmax),y_range=(ymin,ymax))
plot.circle(x='x',y='y',fill_alpha=0.8,source=source,size=8,
            color=dict(field='region',transform=color_mapper),
            legend = 'region')
plot.xaxis.axis_label ='Fertility (children per woman)'
plot.yaxis.axis_label = 'Life Expectancy (years)'
plot.legend.location = 'top_right'
plot.add_tools(hover,box_select,lasso_select)

#### LAYOUT ####
layout = row(widgetbox(slider,x_select,y_select),plot)
curdoc().add_root(layout)
curdoc().title = 'Gapminder'
