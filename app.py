import dash
import requests

from dash import html
from dash import dcc
from dash.dependencies import Input, Output

import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import os

# Creating Data for my app

# weatwaves
disaster_path = "https://raw.githubusercontent.com/soniasocadagui/mdaheroku/main/dat/disaster_data.xlsx"
colslist = ['Year', 'Disaster Type','Disaster Subtype','Country','Start Month','Start Day','End Month','End Day']
disaster_data = pd.read_excel(disaster_path, usecols = colslist)
heatWaves_data = disaster_data[disaster_data['Disaster Subtype'] == 'Heat wave']
# total number disasters
number_disasters = disaster_data[disaster_data['Disaster Type'] == 'Extreme temperature'].groupby(['Country', 'Disaster Subtype']).count().reset_index()[["Country", 'Disaster Subtype', 'Year']]


# temperatures
temperature_path = "https://raw.githubusercontent.com/soniasocadagui/mdaheroku/main/dat/weather_data.csv"
temperature_data = pd.read_csv(temperature_path, sep = ";")
temperature_data = pd.melt(temperature_data, id_vars="utc_timestamp")

average_tem = pd.read_csv("https://raw.githubusercontent.com/soniasocadagui/mdaheroku/main/dat/averageTemMonth.csv")


# Production

production_path = "https://raw.githubusercontent.com/soniasocadagui/mdaheroku/main/dat/production_indices.csv"
production_data = pd.read_csv(production_path, sep = ",")
meanProduction = production_data[production_data['Item']=="Food"]['Value'].mean()


# data Soni

df_total = pd.read_csv("https://raw.githubusercontent.com/soniasocadagui/mdaheroku/main/dat/data_total.csv",
                           sep=",", low_memory=False)

url = "https://raw.githubusercontent.com/soniasocadagui/mdaheroku/main/dat/low_res_custom.geo.json"
f = requests.get(url)
countries = f.json()

# creating the app


app = dash.Dash(__name__, )
server = app.server

app.layout = html.Div([
    html.Div([

        # Logo and title
        html.Div([
            html.Img(src=app.get_asset_url('heat-logo-1.jpg'),
                     id='heat-image',
                     style={'height': '100px',
                            'width': 'auto',
                            'margin-bottom': '25px'})

        ], className='one-third column'),
        html.Div([
            html.Div([
                html.H1('MDA PROJECT', style={'margin-bottom': '0px', 'color': 'white'}),
                html.H5('', style={'margin-bottom': '0px', 'color': 'white'})
            ])

        ], className='one-half column', id='title')

    ], id='header', className='row flex-display', style={'margin-bottom': '25px'}),

    # First panel
    html.Div([

        html.Div([
            html.P('Place the cursor over the country:', className='fix_label', style={'color': 'white'}),
            dcc.Graph(
                id='temp_map',
                hoverData={'points': [{'customdata': 'Belgium'}]}
            )
        ], className='create_container seven columns'),
        # , style={'width': '60%', 'display': 'inline-block', 'padding': '0 20'}),

        html.Div([
            html.P('Select the product:', className='fix_label', style={'color': 'white'}),
            dcc.Dropdown(id="slct_item",
                         options=[
                             {"label": "Agriculture", "value": 'Agriculture'},
                             {"label": "Cereals", "value": 'Cereals'},
                             {"label": "Crops", "value": 'Crops'},
                             {"label": "Food", "value": 'Food'},
                             {"label": "Livestock", "value": 'Livestock'},
                             {"label": "Meat Indigenous", "value": 'Meat Indigenous'},
                             {"label": "Milk", "value": 'Milk'},
                             {"label": "Non-Food", "value": 'Non-Food'},
                             {"label": "Oilcrops", "value": 'Oilcrops'},
                             {"label": "Roots and Tubers", "value": 'Roots and Tubers'},
                             {"label": "Sugar Crops", "value": 'Sugar Crops'},
                             {"label": "Vegetables and Fruits", "value": 'Vegetables and Fruits'}],
                         multi=False,
                         value="Food",
                         style={'width': "60%"}
                         ),

            dcc.Graph(id='x-time-series'),
            dcc.Graph(id='y-time-series'),

        ], className='create_container five columns')  # style={'display': 'inline-block', 'width': '40%'})

    ]),

    html.Div([
        html.Img(src=app.get_asset_url('heat-logo-4.jpg'),
                 id='heat-image2',
                 style={'height': '145px',
                        'width': 'auto',
                        'margin-bottom': '25px'})
    ]),

    # Second panel
    html.Div([
        html.Div([
            html.P('Select Country:', className='fix_label', style={'color': 'white'}),
            dcc.Dropdown(id='w_countries',
                         multi=False,
                         searchable=True,
                         value='Belgium',
                         placeholder='Select Country',
                         options=[{'label': c, 'value': c}
                                  for c in (disaster_data["Country"].unique())], className='dcc_compon')

        ], className='create_container three columns'),

        html.Div([
            dcc.Graph(id='pie_chart', config={'displayModeBar': 'hover'})
        ], className='create_container four columns')
        # ,

        #  html.Div([
        #     dcc.Graph(id = 'heat_chart', config={'displayModeBar': 'hover'})
        #    ], className='create_container five columns')

    ], className='row flex-display'),
    # Counting
    html.Div([
        html.Div([
            html.H6(children='Number Heat Waves',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{heatWaves_data.count().iloc[0]:,.0f}",
                   style={'textAlign': 'center',
                          'color': '#DC143C',
                          'fontSize': 40})

        ], className='card_container three columns'),
        html.Div([
            html.H6(children='Minimum temperature',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(
                f"{temperature_data[temperature_data['value'] == temperature_data['value'].min()]['value'].reset_index()['value'].iloc[0]:,.1f}",
                style={'textAlign': 'center',
                       'color': 'blue',
                       'fontSize': 40})

        ], className='card_container three columns'),
        html.Div([
            html.H6(children='Maximum temperature',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(
                f"{temperature_data[temperature_data['value'] == temperature_data['value'].max()]['value'].reset_index()['value'].iloc[0]:,.1f}",
                style={'textAlign': 'center',
                       'color': 'red',
                       'fontSize': 40})

        ], className='card_container three columns'),
        html.Div([
            html.H6(children='Average gross Per capita PIN',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            html.P(f"{meanProduction:,.1f}",
                   style={'textAlign': 'center',
                          'color': 'green',
                          'fontSize': 40})

        ], className='card_container three columns')

    ], className='row flex display')

], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'})


@app.callback(Output('pie_chart', 'figure'),
              [Input('w_countries', 'value')])
def disasters(w_countries):
    number_disastersA = number_disasters.pivot(index='Country', columns='Disaster Subtype', values='Year').reset_index()

    if number_disastersA[number_disastersA['Country'] == w_countries].shape[0] == 0:
        value_heat = 0
        value_cold = 0
        value_seve = 0
    else:
        value_heat = number_disastersA[number_disastersA['Country'] == w_countries]['Heat wave'].iloc[0]
        value_cold = number_disastersA[number_disastersA['Country'] == w_countries]['Cold wave'].iloc[0]
        value_seve = number_disastersA[number_disastersA['Country'] == w_countries]['Severe winter conditions'].iloc[0]
    colors = ['#FB5A62', '#B6E2F5', '#E3E7EE']
    return {
        'data': [go.Pie(
            labels=['Heat waves', 'Cold waves', 'Severe winter conditions'],
            values=[value_heat, value_cold, value_seve],
            marker=dict(colors=colors),
            hoverinfo='label+value+percent',
            textinfo='label+value',
            hole=.5
        )],

        'layout': go.Layout(
            title={'text': 'Number of Extreme temperature disasters: ' + (w_countries),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 15},
            hovermode='closest',
            paper_bgcolor='#8e9fbc',
            plot_bgcolor='#8e9fbc',
            legend={'orientation': 'h',
                    'bgcolor': '#8e9fbc',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7}

        )
    }

@app.callback(
    Output('temp_map', 'figure'),
    Input('slct_item', 'value'))
def update_figure(selected_item):
    cols = ['country', 'year', 'max_temperature_change', 'code', 'population', 'continent']
    years = [1961, 1970, 1980, 1990, 2000, 2010, 2020]
    dff = df_total.loc[df_total['year'].isin(years), cols].drop_duplicates().reset_index(drop=True)

    fig = px.choropleth_mapbox(dff,
                               geojson=countries,
                               featureidkey="properties.admin",
                               color="max_temperature_change",
                               color_continuous_scale="Viridis",
                               range_color=(0, 9),
                               animation_frame="year",
                               locations="country",
                               hover_name="country",
                               hover_data=["country"],
                               center={"lat": 45.866667, "lon": 10.566667},
                               mapbox_style="open-street-map",
                               zoom=0.1,
                               width=620,
                               height=580,
                               labels={'max_temperature_change': 'Maximum temperature change'}
                               )
    fig.update_layout(title="Maximum Temperature Change by year")
    fig.update_layout(coloraxis_colorbar_title_text='')

    return fig


###############################################

def create_time_series_x(df_dev, title):
    fig = px.line(df_dev, x='year', y='gross_pin', markers=True,
                  labels={
                      "year": "Year",
                      "gross_pin": "Gross PIN"
                  })

    fig.update_layout(title_text=title, title_x=0.5)
    fig.update_layout(height=270, margin={'l': 20, 'b': 30, 'r': 10, 't': 40})

    return fig


@app.callback(
    Output('x-time-series', 'figure'),
    Input('temp_map', 'hoverData'),
    Input('slct_item', 'value'))
def update_x_timeseries(hoverData, xaxis_column_name):
    country = hoverData['points'][0]['customdata']

    if country != "Belgium":
        country_name = country[0]
    else:
        country_name = country

    dff = df_total[df_total['country'] == country_name]
    dff = dff[dff['item'] == xaxis_column_name]
    title = '<b>{}</b>'.format(country_name)
    return create_time_series_x(dff, title)


###############################################

def create_time_series_y(df_dev):
    fig = px.line(df_dev, x='year', y='max_temperature_change',
                  markers=True,
                  labels={
                      "year": "Year",
                      "max_temperature_change": "Max. temperature change"})

    fig.update_layout(height=270, margin={'l': 20, 'b': 30, 'r': 10, 't': 40})

    return fig


@app.callback(
    Output('y-time-series', 'figure'),
    Input('temp_map', 'hoverData'))
def update_y_timeseries(hoverData):
    country = hoverData['points'][0]['customdata']

    if country != "Belgium":
        country_name = country[0]
    else:
        country_name = country

    cols = ['country', 'year', 'max_temperature_change', 'code', 'population', 'continent']
    dff = df_total.loc[:, cols].drop_duplicates().reset_index(drop=True)

    dff = dff[dff['country'] == country_name]

    title = '<b>{}</b>'.format(country_name)
    return create_time_series_y(dff)


if __name__ == '__main__':
    app.run(debug=True, port=(os.getenv("PORT", "1010")))
