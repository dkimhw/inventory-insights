
import dash
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import services.dash_app_data as d
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from datetime import date
import dash_bootstrap_components as dbc

# print(d.query_inventory_data())

app = dash.Dash(
    external_stylesheets=[dbc.themes.COSMO]
)


####################
# Load Data
####################





####################
# Graphs
####################


#########
# Tiles
#########

# Creates a graph object that displays avg car price based on last scraped month
current_month_avg_inventory_price = dcc.Graph(
    id = 'current_month_avg_inventory_price',
    figure = {
        'data': [
            go.Indicator(
                mode = "number",
                value = d.avg_price_last_scraped_month()
            )
        ],
        'layout': go.Layout(
            title = 'Avg Inventory Price',
            height = 250
        )
    }
)

#########
# Avg Year
#########

current_month_avg_inventory_make_year = dcc.Graph(
    id = 'current_month_avg_inventory_make_year',
    figure = {
        'data': [
            go.Indicator(
                mode = "number",
                value = d.avg_vehicle_year('2022-06-01', '2022-07-30')
            )
        ],
        'layout': go.Layout(
            title = 'Avg Inventory Make Year',
            height = 250
        )
    }
)

@app.callback(
    Output('current_month_avg_inventory_make_year', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
def update_avg_make_year_chart (start_date, end_date):
    """
       start_date: The start date chosen by the user via dash callback
       end_dte: The end date chosen by the user via dash callback

        Returns: Plotly graph object
    """
    print(d.avg_vehicle_year(start_date, end_date))
    fig =  {
            'data': [
                go.Indicator(
                    mode = "number",
                    value = d.avg_vehicle_year(start_date, end_date)
                )
            ],
            'layout': go.Layout(
                title = 'Avg Inventory Make Year',
                height = 250
            )
    }


    return fig


#########
# Count of Makes Bar Chart
#########

count_of_makes_data = d.make_count('2022-06-01', '2022-07-30')
make_bar_chart = dcc.Graph(
    id = 'count_of_vehicles_by_makes',
    figure = px.bar(
        count_of_makes_data,
        y='vin',
        x='make',
        text_auto='.2s',
        title="Count of Used Cars by Make Stocked by Dealerships",
        labels={ # replaces default labels by column name
            "vin": "Count of Vehicles", "make": "Make"
        }
    )
)

@app.callback(
    Output('count_of_vehicles_by_makes', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
def update_make_bar_chart (start_date, end_date):
    """
       start_date: The start date chosen by the user via dash callback
       end_dte: The end date chosen by the user via dash callback

        Returns: Plotly graph object
    """
    makes_data = d.make_count(start_date, end_date)
    fig = px.bar(
        makes_data,
        y='vin',
        x='make',
        text_auto='.2s',
        title="Count of Used Cars by Make Stocked by Dealerships",
        labels={ # replaces default labels by column name
            "vin": "Count of Vehicles", "make": "Make"
        }
    )

    return fig


####################
## Main Layout
####################

app.layout = dash.html.Div([
    # Overall fatal accidents and incidents trends
    dash.html.H1("Dealership Data Overview", className="section-title"),
    dbc.Row(
        dbc.Col(
            dcc.DatePickerRange(
                id='date-picker-range',
                min_date_allowed=date(2022, 1, 1),
                initial_visible_month=date(2022, 6, 1),
                start_date= date(2022, 6, 1),
                end_date=date(2022, 7, 31)
            ),
            width={"size": 6},
        ), justify="center"
    ),
    dbc.Row(
        [
            dbc.Col(html.Div(current_month_avg_inventory_price)),
            dbc.Col(html.Div(current_month_avg_inventory_make_year)),
            dbc.Col(html.Div("One of three columns")),
        ], align="center"
    ),




    make_bar_chart
])







# Run the Dash App
if __name__ == '__main__':
  app.run_server(debug=True)
