from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import sqlite3

# ____________________________________________________________________________________ SQLite3 Integration

# Read sqlite query results into a pandas DataFrame
con = sqlite3.connect("Sensors Database.db")  # Name of database
df = pd.read_sql_query("SELECT * FROM Sensors_Database", con)  # Name of Table inside the database.  #Select * From = means everything from that table
#
# # Verify that result of SQL query is stored in the dataframe
print(df.head())  # print the database table in Console
#
con.close()

app = Dash(__name__)

app.layout = html.Div([

    html.H1("UAS Operations: Air Quality Monitoring Dashboard"),
    html.H1("Location: Modesto California"),

    # start of dashboard

html.Button("Render data-points form CSV ", n_clicks=0, id='button'),


    # Need an input and naming the title of the graph and Graph ID
    html.H4('PM_1 Particulate Concentrations over time'),  # html headings for graphs titles
    dcc.Graph(id="PM_1_Sensor"),
    html.H4('Air Quality'),
    dcc.Graph(id="Air_Quality"),
    html.H4('PM_4 Particulate Concentrations over time'),
    dcc.Graph(id="PM_4_Sensor"),
    html.H4('Fugitive Particulate Concentrations over time'),
    dcc.Graph(id="PM_10_Sensor"),
    html.H4("Triple Super-phosphate over time "),
    dcc.Graph(id="TSP_Sensor"),
    html.H4("Sensors Location with readings"),
    dcc.Graph(id="fig_mapbox")

])


@app.callback(
    Output("PM_1_Sensor", "figure"),
    Output("Air_Quality", "figure"),
    Output("PM_4_Sensor", "figure"),
    Output("PM_10_Sensor", "figure"),
    Output("TSP_Sensor", "figure"),
    Output("fig_mapbox", "figure"),
    Input("button", "n_clicks"),
    #    Input("Sql_integration", "n_clicks")
)
def display_graph(n_clicks):  # Renders the graph data-points

    x_pm_1, y_pm_1 = 'Time', 'PM_1'
    x_aq, y_aq = 'Time', 'PM_2.5'
    x_pm_4, y_pm_4 = 'Time', 'PM_4'
    x_pm_10, y_pm_10 = 'Time', 'PM_10'
    x_pm_tsp, y_pm_tsp = 'Time', 'TSP'

    fig_pm_1 = px.line(df, x=x_pm_1, y=y_pm_1)  # Shows the type of graph and what data-points are plotted.
    fig_aq = px.line(df, x=x_aq, y=y_aq)
    fig_pm_4 = px.line(df, x=x_pm_4, y=y_pm_4)
    fig_pm_10 = px.line(df, x=x_pm_10, y=y_pm_10)
    fig_pm_tsp = px.line(df, x=x_pm_tsp, y=y_pm_tsp)






    # Map Rendering of CSV file
    fig_mapbox = px.scatter_mapbox(df, lat="lat", lon="lon", hover_data=["PM_1", "PM_2.5", "PM_4", "PM_10", "TSP"],
                                   color_discrete_sequence=["fuchsia"], zoom=15, height=500)

    fig_mapbox.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[
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
        ])
    fig_mapbox.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                             mapbox=dict(center=dict(lat=36.498, lon=-119.383)))

    return fig_pm_1, fig_aq, fig_pm_4, fig_pm_10, fig_pm_tsp, fig_mapbox  # To display all graphs on a single page follow by a comma.


if __name__ == '__main__':  # Dash Development Server run on 8050
    app.run_server(debug=True)
