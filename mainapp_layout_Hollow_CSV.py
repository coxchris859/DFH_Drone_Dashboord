import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
import dash_bootstrap_components as dbc

# ____________________________________________________________________________________ SQLite3 Integration

# Read sqlite query results into a pandas DataFrame
#con = sqlite3.connect("Sensors Database.db")  # Name of database
#df = pd.read_sql_query("SELECT * FROM Hollow_Data_1", con)
# Verify that result of SQL query is stored in the dataframe
#con.close()
# print the database table in Console
# drop all nan value
df = pd.read_csv('DutchHollow_07222018_non_nan.csv')

print(df.head())


# ________________________________________________________________
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])

app.layout = dbc.Container([
    dcc.Interval(
        id='six_seconds',
        disabled=False,
        interval=1 * 6000,
        n_intervals=4,
        max_intervals=4,
    ),
    dbc.Row(html.P("UAS Operations: Air Quality Monitoring Dashboard"),  # title Bar
            className='text-left'),
    dbc.Row(html.P("Location: Modesto California"), className='text-left'),  # title Bar
    #    dbc.Row(html.Img(src="DFH_Logo.png", height="150px")),  # File name logo.png
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([html.P("Air Quality",
                                style={"textDecoration": "underline"})]),
                dcc.Graph(id="Air_Quality", style={'height': 145},
                          config={'displayModeBar': False})
            ]),
            dbc.Row([
                dbc.Col([html.P("Fugitive Particulate Concentrations",
                                style={"textDecoration": "underline"})]),
                dcc.Graph(id="PM_10_Sensor", style={'height': 100},
                          config={'displayModeBar': False})
            ]),
            dbc.Row([
                dbc.Col([html.P("Volatile Organic Compounds ",
                                style={"textDecoration": "underline"})]),
                dcc.Graph(id="Volatile Organic Compounds", style={'height': 100})
            ]),
            dbc.Row([
                dbc.Col([html.P("Temperature ",
                                style={"textDecoration": "underline"})]),
                dcc.Graph(id="Temperature", style={'height': 100})
            ]),
            dbc.Row([
                dbc.Col([html.P("Pressure Sensor",
                                style={"textDecoration": "underline"})]),
                dcc.Graph(id="Pressure", style={'height': 100})
            ]),
            dbc.Row([
                dbc.Col([html.P("Humidity Sensor",
                                style={"textDecoration": "underline"})]),
                dcc.Graph(id="Humidity", style={'height': 100})
            ]),

        ], width=3),
        dbc.Col([
            dbc.Row([
                dbc.Col([html.P("Plotting Sensors on Map",
                                style={"textDecoration": "underline"})]),
                dcc.Graph(id="fig_mapbox")
            ]),
            dbc.Row([
                dbc.Col([html.P("RangeSlider Placeholder",
                                style={"textDecoration": "underline"})]),
                dcc.RangeSlider(0, 20, 1, value=[5, 15], id='my-range-slider'),
                html.Div(id='output-container-range-slider'),

            ]),
            dbc.Row([
                dbc.Col([html.P("Altitude Reading",
                                style={"textDecoration": "underline"})]),
                dcc.Graph(style={'height': 50}),

            ])

        ], width=9)

    ])

])


@app.callback(
    Output("Air_Quality", "figure"),
    Output("PM_10_Sensor", "figure"),
    Output("Volatile Organic Compounds", "figure"),
    Output("Temperature", "figure"),
    Output("Pressure", "figure"),
    Output("Humidity", "figure"),
    Output("fig_mapbox", "figure"),
    Input("six_seconds", "n_intervals"))
def display_graph(n_clicks):  # Renders the graph data-points

    x_aq, y_aq = 'gps_date', 'standard_pm2_5'
    x_pm_10, y_pm_10 = 'gps_date', 'standard_pm10'
    x_voc, y_voc = 'Voc', 'gps_date'
    x_temp, y_temp = 'gps_date', 'Temperature'
    x_pressure, y_pressure = 'gps_date', 'Pressure'
    x_hum, y_hum = 'gps_date', 'Humidity'

    fig_aq = px.line(df, x=x_aq, y=y_aq, range_x=[])
    fig_aq.update_xaxes(showticklabels=False, title=None)
    fig_aq.update_yaxes(title='AQI')
    fig_aq.update_xaxes(title='Time')
    fig_aq.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    fig_aq.update_yaxes(range=[0, 200])
    fig_aq.add_hrect(y0=150, y1=200, line_width=0, fillcolor="red", opacity=0.2)
    fig_aq.add_hrect(y0=100, y1=150, line_width=0, fillcolor="orange", opacity=0.2)
    fig_aq.add_hrect(y0=50, y1=100, line_width=0, fillcolor="yellow", opacity=0.2)
    fig_aq.add_hrect(y0=0, y1=50, line_width=0, fillcolor="green", opacity=0.2)

    fig_pm_10 = px.line(df, x=x_pm_10, y=y_pm_10, range_x=[])  # PM10
    fig_pm_10.update_xaxes(showticklabels=False, title='PM 10 um/m3')
    fig_pm_10.update_yaxes(title='PM 10 um/m3')
    fig_pm_10.update_xaxes(title='Time')
    fig_pm_10.update_layout(margin=dict(l=10, r=10, t=10, b=10))
#    fig_pm_10.update_yaxes(range=[15, 50])

    fig_voc = px.line(df, x=x_voc, y=x_voc, range_x=[])  # voc
    fig_voc.update_xaxes(showticklabels=False)
    fig_voc.update_xaxes(showticklabels=False, title=None)
    fig_voc.update_yaxes(title='%VOC')
    fig_voc.update_xaxes(title='Time')
    fig_voc.update_layout(margin=dict(l=10, r=10, t=10, b=10))

    fig_temperature = px.line(df, x=x_temp, y=y_temp, range_x=[])  # Temp
    fig_temperature.update_xaxes(showticklabels=False, title=None)
    fig_temperature.update_yaxes(title='Fahrenheit')
    fig_temperature.update_xaxes(title='Time')
    fig_temperature.update_layout(margin=dict(l=10, r=10, t=10, b=10))

    fig_pressure = px.line(df, x=x_pressure, y=y_pressure)
    fig_pressure.update_xaxes(showticklabels=False, title=None)
    fig_pressure.update_yaxes(title='Pa')
    fig_pressure.update_xaxes(title='Time')
    fig_pressure.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    # Pressure

    fig_hum = px.line(df, x=x_hum, y=y_hum)  # Humidty
    fig_hum.update_xaxes(showticklabels=False, title=None)
    fig_hum.update_yaxes(title='RH%')
    fig_hum.update_xaxes(title='Time')
    fig_hum.update_layout(margin=dict(l=10, r=10, t=10, b=10))

    fig_mapbox = px.density_mapbox(df, lat="latitude", lon="longitude", z="standard_pm2_5",
                                   hover_data=["alt", "standard_pm1_0"], zoom=15, height=500)
    fig_mapbox.update_layout(mapbox_style="white-bg", mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        },
        {
            "sourcetype": "raster",
            "sourceattribution": "Government of Canada",
            "source": ["https://geo.weather.gc.ca/geomet/?"
                       "SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX={bbox-epsg-3857}&CRS=EPSG:3857"
                       "&WIDTH=1000&HEIGHT=1000&LAYERS=RADAR_1KM_RDBR&TILED=true&FORMAT=image/png"],
        }
    ]),
    fig_mapbox.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                             mapbox=dict(center=dict(lat=36.498, lon=-119.383)))

    return fig_aq, fig_pm_10, fig_voc, fig_temperature, fig_pressure, fig_hum, fig_mapbox


if __name__ == '__main__':  # Dash Development Server run on 8050
    app.run_server(debug=True)
