
import dash
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import services.query as q

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
                value = q.avg_price_current_month()
            )
        ],
        'layout': go.Layout(
            title = 'Current Month Avg Inventory Price',
            height = 250
        )
    }
)



####################
## Main Layout
####################

app.layout = dash.html.Div([
    # Overall fatal accidents and incidents trends
    dash.html.H1("General Trends Between Time Periods", className="section-title"),

    current_month_avg_inventory_price
])







# Run the Dash App
if __name__ == '__main__':
  app.run_server(debug=True)
