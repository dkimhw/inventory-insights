
import dash
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import services.dash_app_data as d
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from datetime import date
import dash_bootstrap_components as dbc
import datetime
from app import app


##################################################
# Starting Variables
##################################################


end_date =  datetime.date.today()
start_date = datetime.date(end_date.year, end_date.month - 5, 1).strftime("%Y-%m-%d")
end_date = end_date.strftime("%Y-%m-%d")

indicator_chart_height = 200
indicator_font_size = 32


##################################################
# Graphs
##################################################


##################################################
# Tile: Average Inventory Price
##################################################

# Creates a graph object that displays avg car price based on last scraped month
avg_inventory_price = dcc.Graph(
    id = 'avg_inventory_price',
    figure = {
        'data': [
            go.Indicator(
                mode = "number",
                value = d.avg_inventory_price(start_date, end_date),
                number={"font":{"size": indicator_font_size}},
            )
        ],
        'layout': go.Layout(
            title = 'Average Inventory Price',
            height = indicator_chart_height,
        )
    }
)

@app.callback(
    Output('avg_inventory_price', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
def update_avg_price_indicator_chart (start_date, end_date):
    """
       start_date: The start date chosen by the user via dash callback
       end_dte: The end date chosen by the user via dash callback

        Returns: Plotly graph object
    """
    fig =  {
            'data': [
                go.Indicator(
                    mode = "number",
                    value = d.avg_inventory_price(start_date, end_date),
                    number={"font":{"size": indicator_font_size}},
                )
            ],
            'layout': go.Layout(
                title = 'Average Inventory Price',
            )
    }


    return fig

##################################################
# Tile: Average Inventory Year
##################################################

avg_inventory_make_year = dcc.Graph(
    id = 'avg_inventory_make_year',
    figure = {
        'data': [
            go.Indicator(
                mode = "number",
                value = d.avg_vehicle_year(start_date, end_date),
                number={"font":{"size": indicator_font_size}},
            )
        ],
        'layout': go.Layout(
            title = 'Average Inventory Make Year',
            height = indicator_chart_height
        )
    }
)

@app.callback(
    Output('avg_inventory_make_year', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
def update_avg_make_year_chart (start_date, end_date):
    """
        start_date: The start date chosen by the user via dash callback
        end_dte: The end date chosen by the user via dash callback

        Returns: Plotly graph object
    """
    fig =  {
            'data': [
                go.Indicator(
                    mode = "number",
                    value = d.avg_vehicle_year(start_date, end_date),
                    number={"font":{"size": indicator_font_size}},
                )
            ],
            'layout': go.Layout(
                title = 'Average Inventory Make Year',
                height = indicator_chart_height
            )
    }


    return fig


##################################################
# Tile: Average Inventory Mileage
##################################################

avg_inventory_mileage = dcc.Graph(
    id = 'avg_inventory_mileage',
    figure = {
        'data': [
            go.Indicator(
                mode = "number",
                value = d.avg_vehicle_mileage(start_date, end_date),
                number={"font":{"size": indicator_font_size}},
            )
        ],
        'layout': go.Layout(
            title = 'Average Inventory Mileage',
            height = indicator_chart_height
        )
    }
)

@app.callback(
    Output('avg_inventory_mileage', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
def update_avg_inventory_mileage (start_date, end_date):
    """
        start_date: The start date chosen by the user via dash callback
        end_dte: The end date chosen by the user via dash callback

        Returns: Plotly graph object
    """
    fig =  {
            'data': [
                go.Indicator(
                    mode = "number",
                    value = d.avg_vehicle_mileage(start_date, end_date),
                    number={"font":{"size": indicator_font_size}},
                )
            ],
            'layout': go.Layout(
                title = 'Average Inventory Mileage'
            )
    }
    return fig


##################################################
# Count of Makes Bar Chart
##################################################

make_bar_chart = dcc.Graph(
    id = 'count_of_vehicles_by_makes',
    figure = px.bar(
        d.make_count(start_date, end_date),
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
        title="Count of Used Cars by Make",
        labels={ # replaces default labels by column name
            "vin": "Count of Vehicles", "make": "Make"
        }
    )

    return fig

##################################################
# Avg Price by Month Line Chart
##################################################

avg_price_line_chart = dcc.Graph(
    id = 'avg_price_by_month_line_chart',
    figure = px.line(
        d.avg_price_by_month('2022-01-01', end_date),
        x='inventory_month',
        y='price',
        title="Average Inventory Price by Month",
        labels={ # replaces default labels by column name
            "inventory_month": "Inventory Month", "price": "Avg Inventory Price"
        }
    )
)

@app.callback(
    Output('avg_price_by_month_line_chart', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
def update_avg_price_line_chart(start_date, end_date):
    """
       start_date: The start date chosen by the user via dash callback
       end_dte: The end date chosen by the user via dash callback

        Returns: Plotly graph object
    """
    line_chart_data = d.avg_price_by_month(start_date, end_date)
    fig = px.line(
        line_chart_data,
        x='inventory_month',
        y='price',
        title="Average Inventory Price by Month",
        labels={ # replaces default labels by column name
            "inventory_month": "Inventory Month", "price": "Avg Inventory Price"
        }
    )

    return fig

##################################################
# Avg Delaership Inventory Size by Month Line Chart
##################################################

avg_dealership_inventory_size_by_month_line_chart = dcc.Graph(
    id = 'avg_dealership_inventory_size_by_month_line_chart',
    figure = px.line(
        d.avg_dealership_inventory_size_by_month('2022-01-01', end_date),
        x='inventory_month',
        y='inventory_size',
        title="Average Dealership Inventory Size by Month",
        labels={ # replaces default labels by column name
            "inventory_month": "Inventory Month", "inventory_size": "Average Inventory Size per Dealership"
        }
    )
)

@app.callback(
    Output('avg_dealership_inventory_size_by_month_line_chart', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
def update_avg_dealership_inventory_size_line_chart(start_date, end_date):
    """
       start_date: The start date chosen by the user via dash callback
       end_dte: The end date chosen by the user via dash callback

        Returns: Plotly graph object
    """
    line_chart_data = d.avg_dealership_inventory_size_by_month(start_date, end_date)
    fig = px.line(
        line_chart_data,
        x='inventory_month',
        y='inventory_size',
        title="Average Dealership Inventory Size by Month",
        labels={ # replaces default labels by column name
            "inventory_month": "Inventory Month", "inventory_size": "Average Inventory Size per Dealership"
        }
    )

    return fig

##################################################
# Count of Makes by Month Line Chart
##################################################

make_month_line_chart = dcc.Graph(
    id = 'count_of_vehicles_by_makes_and_month',
    figure = px.line(
        d.make_count_by_month(start_date, end_date),
        y='vin',
        x='inventory_month',
        color="make",
        title="Count of Used Cars by Inventory Month & Make (Top 10 Makes Only)",
        labels={ # replaces default labels by column name
            "vin": "Count of Vehicles", "inventory_month": "Inventory Month"
        }
    )
)

@app.callback(
    Output('count_of_vehicles_by_makes_and_month', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
def update_make_month_line_chart(start_date, end_date):
    """
       start_date: The start date chosen by the user via dash callback
       end_dte: The end date chosen by the user via dash callback

       Returns: Plotly graph object
    """
    make_month_data = d.make_count_by_month(start_date, end_date)
    fig = px.line(
        make_month_data,
        y='vin',
        x='inventory_month',
        color="make",
        title="Count of Used Cars by Inventory Month & Make (Top 10 Makes Only)",
        labels={ # replaces default labels by column name
            "vin": "Count of Vehicles", "inventory_month": "Inventory Month"
        }
    )

    return fig

##################################################
# Transmission Type Count Bar Chart
##################################################

transmission_bar_chart = dcc.Graph(
    id = 'count_of_vehicles_by_transmission',
    figure = px.bar(
        d.transmission_type_count(start_date, end_date),
        y='count_of_vehicles',
        x='transmission',
        text_auto='.2s',
        title="Count of Used Cars by Transmission",
        labels={ # replaces default labels by column name
            "count_of_vehicles": "Count of Vehicles", "transmission": "Transmission Type"
        }
    )
)

@app.callback(
    Output('transmission_bar_chart', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
def update_transmission_bar_chart (start_date, end_date):
    """
       start_date: The start date chosen by the user via dash callback
       end_dte: The end date chosen by the user via dash callback

        Returns: Plotly graph object
    """
    data = d.transmission_type_count(start_date, end_date)
    fig = px.bar(
        data,
        y='count_of_vehicles',
        x='transmission',
        text_auto='.2s',
        title="Count of Used Cars by Transmission",
        labels={ # replaces default labels by column name
            "count_of_vehicles": "Count of Vehicles", "transmission": "Transmission Type"
        }
    )

    return fig

##################################################
# Vehicle Year Count Bar Chart
##################################################

vehicle_year_bar_chart = dcc.Graph(
    id = 'count_of_vehicles_by_vehicle_year',
    figure = px.bar(
        d.vehicle_year_count(start_date, end_date),
        y='count_of_vehicles',
        x='year',
        text_auto='.2s',
        title="Count of Used Cars by Vehicle Year",
        labels={ # replaces default labels by column name
            "count_of_vehicles": "Count of Vehicles", "year": "Vehicle Year"
        }
    )
)

@app.callback(
    Output('count_of_vehicles_by_vehicle_year', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
def update_vehicle_year_bar_chart (start_date, end_date):
    """
       start_date: The start date chosen by the user via dash callback
       end_dte: The end date chosen by the user via dash callback

        Returns: Plotly graph object
    """
    data = d.vehicle_year_count(start_date, end_date)
    fig = px.bar(
        data,
        y='count_of_vehicles',
        x='year',
        text_auto='.2s',
        title="Count of Used Cars by Vehicle Year",
        labels={ # replaces default labels by column name
            "count_of_vehicles": "Count of Vehicles", "year": "Vehicle Year"
        }
    )

    return fig


####################
## Main Layout
####################

layout = dash.html.Div([

    # Navbar
    dash.html.Div([
        dash.html.H1("Summary", className="dashboard-title")
    ], className="dashboard-title-section"),

    # Dashboard body
    dash.html.Div([
        # Filter section
        dbc.Row(
            dbc.Col(
                dcc.DatePickerRange(
                    id='date-picker-range',
                    min_date_allowed=date(2022, 1, 1),
                    initial_visible_month=start_date,
                    start_date=start_date,
                    end_date=end_date
                ),
                width={"size": 6},
            ), justify="flex-start", className="dashboard-filter-section"
        ),

        dash.html.Div(
            [
                dash.html.Div(avg_inventory_price, className="indicator-chart"),
                dash.html.Div(avg_inventory_make_year, className="indicator-chart"),
                dash.html.Div(avg_inventory_mileage, className="indicator-chart"),
            ], className="indicator-chart-section"
        ),

        make_bar_chart,
        avg_price_line_chart,
        avg_dealership_inventory_size_by_month_line_chart,
        make_month_line_chart,
        transmission_bar_chart,
        vehicle_year_bar_chart
    ], className="dashboard-body")

])
