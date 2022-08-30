
# Import necessary libraries
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from app import app
import datetime
import services.dash_app_data as d
from dash import dcc

##################################################
# Starting Variables
##################################################

end_date =  datetime.date.today()
start_date = datetime.date(end_date.year, end_date.month - 5, 1).strftime("%Y-%m-%d")
end_date = end_date.strftime("%Y-%m-%d")

##################################################
# Avg Price by Month Line Chart
##################################################

avg_price_line_chart = dash.dcc.Graph(
  id = 'avg_price_by_month_line_chart2',
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
  Output('avg_price_by_month_line_chart2', 'figure'),
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


# Define the page layout
layout = dbc.Container([
    # Title section
    dash.html.Div([
        dash.html.H1("Vehicle Make Detailed Overview", className="dashboard-title")
    ], className="dashboard-title-section"),

    # Filter section
    dash.html.Div([
      dash.html.Div([
        dash.html.Label("Inventory Date Range"),
        dash.dcc.DatePickerRange(
            id='date-picker-range',
            min_date_allowed=datetime.date(2022, 1, 1),
            initial_visible_month=start_date,
            start_date=start_date,
            end_date=end_date,
            className="filter-input"
        )
      ], className="filter-group"),
      dash.html.Div([
        dash.html.Label("Vehicle Make"),
        dash.dcc.Dropdown(
          id="make-dropdown",
          options= ['New York City', 'Montreal', 'San Francisco'],
          multi=True,
          className="filter-input",
          style={"width": "100%"}
        )
      ], className="filter-group"),
    ], className="filter-section"),

    avg_price_line_chart
])
