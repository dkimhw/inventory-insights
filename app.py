
import dash
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import services.dash_app_data as d
import plotly.express as px

# print(d.query_inventory_data())

app = dash.Dash(__name__)


####################
# Load Data
####################





####################
# Static Graphs
####################

# Display avg car price based on last scraped month
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
            title = 'Current Month Avg Inventory Price',
            height = 250
        )
    }
)

# print(d.make_bar_char_count('2022-06-01', '2022-07-30'))
# Static Bar Chart by Make

"""
make_bar_chart = dcc.Graph(
    id = 'count_of_vehicles_by_makes',
    figure = {
        'data': [
            go.Bar(
                x=list(count_of_makes_data['make']),
                y=list(count_of_makes_data['vin'])
                # x = count_of_makes_data['make'],
                # y = count_of_makes_data['vin']
            )
        ],
        'layout': go.Layout(
            title = 'Count of Used Cars by Make Stocked by Dealerships',
            height = 250
        )
    }
)

    fig = px.bar(df, y='pop', x='country', text_auto='.2s',
            title="Default: various text sizes, positions and angles")
"""

count_of_makes_data = d.make_count('2022-06-01', '2022-07-30')
make_bar_chart = dcc.Graph(
    id = 'count_of_vehicles_by_makes',
    figure = px.bar(count_of_makes_data, y='vin', x='make', text_auto='.2s', title="Count of Used Cars by Make Stocked by Dealerships")
)


####################
# Filterable Graphs
####################





####################
## Main Layout
####################

app.layout = dash.html.Div([
    # Overall fatal accidents and incidents trends
    dash.html.H1("General Trends Between Time Periods", className="section-title"),

    current_month_avg_inventory_price,

    make_bar_chart
])







# Run the Dash App
if __name__ == '__main__':
  app.run_server(debug=True)
