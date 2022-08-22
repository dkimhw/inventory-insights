
import dash
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import services.dash_app_data as d
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from datetime import date
import dash_bootstrap_components as dbc
import datetime


app = dash.Dash(
    external_stylesheets=[dbc.themes.COSMO]
)

####################
# Starting Variables
####################

end_date =  datetime.date.today()
start_date = datetime.date(end_date.year, end_date.month - 1, 1).strftime("%Y-%m-%d")
end_date = end_date.strftime("%Y-%m-%d")

####################
# Graphs
####################


###########################
# Tile: Average Inventory Price
###########################

# Creates a graph object that displays avg car price based on last scraped month
avg_inventory_price = dcc.Graph(
    id = 'avg_inventory_price',
    figure = {
        'data': [
            go.Indicator(
                mode = "number",
                value = d.avg_inventory_price(start_date, end_date)
            )
        ],
        'layout': go.Layout(
            title = 'Average Inventory Price',
            height = 250
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
    print(d.avg_vehicle_year(start_date, end_date))
    fig =  {
            'data': [
                go.Indicator(
                    mode = "number",
                    value = d.avg_inventory_price(start_date, end_date)
                )
            ],
            'layout': go.Layout(
                title = 'Average Inventory Price',
            )
    }


    return fig

###########################
# Tile: Average Inventory Year
###########################

avg_inventory_make_year = dcc.Graph(
    id = 'avg_inventory_make_year',
    figure = {
        'data': [
            go.Indicator(
                mode = "number",
                value = d.avg_vehicle_year(start_date, end_date)
            )
        ],
        'layout': go.Layout(
            title = 'Average Inventory Make Year',
            height = 250
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
    print(d.avg_vehicle_year(start_date, end_date))
    fig =  {
            'data': [
                go.Indicator(
                    mode = "number",
                    value = d.avg_vehicle_year(start_date, end_date)
                )
            ],
            'layout': go.Layout(
                title = 'Average Inventory Make Year'
            )
    }


    return fig


###########################
# Tile: Average Inventory Mileage
###########################

avg_inventory_mileage = dcc.Graph(
    id = 'avg_inventory_mileage',
    figure = {
        'data': [
            go.Indicator(
                mode = "number",
                value = d.avg_vehicle_mileage(start_date, end_date)
            )
        ],
        'layout': go.Layout(
            title = 'Average Inventory Mileage',
            height = 250
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
    print(d.avg_vehicle_year(start_date, end_date))
    fig =  {
            'data': [
                go.Indicator(
                    mode = "number",
                    value = d.avg_vehicle_mileage(start_date, end_date)
                )
            ],
            'layout': go.Layout(
                title = 'Average Inventory Mileage'
            )
    }
    return fig


#########################
# Count of Makes Bar Chart
#########################

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
    dash.html.H1("Dealership Data Overview", className="dashboard-title mb-4"),
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
        ), justify="flex-start", className="mb-2"
    ),
    dbc.Row(
        [
            dbc.Col(html.Div(avg_inventory_price), width={'size': 4}),
            dbc.Col(html.Div(avg_inventory_make_year), width={'size': 4}),
            dbc.Col(html.Div(avg_inventory_mileage), width={'size': 4}),
        ], align="center", justify="center"
    ),

    make_bar_chart
], className="dashboard-body")



# Run the Dash App
if __name__ == '__main__':
  app.run_server(debug=True)
