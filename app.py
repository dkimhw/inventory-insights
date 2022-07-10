
import dash
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import services.dash_app_data as d


# print(d.query_inventory_data())

app = dash.Dash(__name__)


####################
# Load Data
####################





####################
# Static Graphs
####################

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


####################
# Filterable Graphs
####################





####################
## Main Layout
####################

app.layout = dash.html.Div([
    # Overall fatal accidents and incidents trends
    dash.html.H1("General Trends Between Time Periods", className="section-title"),

    current_month_avg_inventory_price
])

print(d.make_bar_char_count('2022-06-01', '2022-07-30'))





# Run the Dash App
if __name__ == '__main__':
  app.run_server(debug=True)
