
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
first_selected = 'Ford'

##################################################
# Avg Price by Month & Make Line Chart
##################################################

avg_price_by_make_line_chart = dash.dcc.Graph(
  id = 'avg_price_by_make_line_chart',
  figure = px.line(
      d.get_avg_price_by_month_and_make('2022-01-01', end_date, [first_selected]),
      x='inventory_month',
      y='price',
      color='make',
      title="Average Inventory Price by Month & Make",
      labels={ # replaces default labels by column name
          "inventory_month": "Inventory Month", "price": "Avg Inventory Price", 'make': 'Make'
      }
  )
)

@app.callback(
  Output('avg_price_by_make_line_chart', 'figure'),
  Input('date-picker-range', 'start_date'),
  Input('date-picker-range', 'end_date'),
  Input('make-dropdown', 'value')
)
def update_avg_price_by_make_line_chart(start_date, end_date, value):
  """
      start_date: The start date chosen by the user via dash callback
      end_dte: The end date chosen by the user via dash callback

      Returns: Plotly graph object
  """
  value = [value] if type(value) != list else value
  line_chart_data = d.get_avg_price_by_month_and_make(start_date, end_date, value)
  fig = px.line(
      line_chart_data,
      x='inventory_month',
      y='price',
      color='make',
      title="Average Inventory Price by Month & Make",
      labels={ # replaces default labels by column name
          "inventory_month": "Inventory Month", "price": "Avg Inventory Price", 'make': 'Make'
      }
  )

  return fig

##################################################
# Avg Mileage by Month & Make Line Chart
##################################################

avg_mileage_by_make_line_chart = dash.dcc.Graph(
  id = 'avg_mileage_by_make_line_chart',
  figure = px.line(
      d.get_avg_mileage_by_month_and_make('2022-01-01', end_date, [first_selected]),
      x='inventory_month',
      y='mileage',
      color='make',
      title="Average Inventory Mileage by Month & Make",
      labels={ # replaces default labels by column name
          "inventory_month": "Inventory Month", "mileage": "Avg Inventory Mileage", 'make': 'Make'
      }
  )
)

@app.callback(
  Output('avg_mileage_by_make_line_chart', 'figure'),
  Input('date-picker-range', 'start_date'),
  Input('date-picker-range', 'end_date'),
  Input('make-dropdown', 'value')
)
def update_avg_mileage_by_make_line_chart(start_date, end_date, value):
  """
      start_date: The start date chosen by the user via dash callback
      end_dte: The end date chosen by the user via dash callback

      Returns: Plotly graph object
  """
  value = [value] if type(value) != list else value
  line_chart_data = d.get_avg_mileage_by_month_and_make(start_date, end_date, value)
  fig = px.line(
      line_chart_data,
      x='inventory_month',
      y='mileage',
      color='make',
      title="Average Inventory Mileage by Month & Make",
      labels={ # replaces default labels by column name
          "inventory_month": "Inventory Month", "mileage": "Avg Inventory Mileage", 'make': 'Make'
      }
  )

  return fig

##################################################
# Avg Vehicle Year by Month & Make Line Chart
##################################################

avg_vehicle_year_by_make_line_chart = dash.dcc.Graph(
  id = 'avg_vehicle_year_by_make_line_chart',
  figure = px.line(
      d.get_avg_vehicle_year_by_month_and_make('2022-01-01', end_date, [first_selected]),
      x='inventory_month',
      y='vehicle_year',
      color='make',
      title="Average Inventory Year by Month & Make",
      labels={ # replaces default labels by column name
          "inventory_month": "Inventory Month", "vehicle_year": "Avg Inventory Year", 'make': 'Make'
      }
  )
)

@app.callback(
  Output('avg_vehicle_year_by_make_line_chart', 'figure'),
  Input('date-picker-range', 'start_date'),
  Input('date-picker-range', 'end_date'),
  Input('make-dropdown', 'value')
)
def update_avg_vehicle_year_by_make_line_chart(start_date, end_date, value):
  """
      start_date: The start date chosen by the user via dash callback
      end_dte: The end date chosen by the user via dash callback

      Returns: Plotly graph object
  """
  value = [value] if type(value) != list else value
  line_chart_data = d.get_avg_vehicle_year_by_month_and_make(start_date, end_date, value)
  fig = px.line(
      line_chart_data,
      x='inventory_month',
      y='vehicle_year',
      color='make',
      title="Average Inventory Year by Month & Make",
      labels={ # replaces default labels by column name
          "inventory_month": "Inventory Month", "vehicle_year": "Avg Inventory Year", 'make': 'Make'
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
          options=d.get_vehicle_makes(),
          multi=True,
          className="filter-input",
          style={"width": "100%"},
          value=first_selected
        )
      ], className="filter-group"),
    ], className="filter-section"),

    avg_price_by_make_line_chart,
    avg_mileage_by_make_line_chart,
    avg_vehicle_year_by_make_line_chart
])
