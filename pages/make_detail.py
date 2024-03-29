
# Import necessary libraries
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
from app import app
import datetime
import services.make_detail_data as d
from dash import dcc
from components import collapse, separator, page_header, info_card


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

@app.callback(
  Output('avg_price_by_make_line_chart', 'children'),
  Input('date-picker-range', 'start_date'),
  Input('date-picker-range', 'end_date'),
  Input('make-dropdown', 'value')
)
def make_avg_price_by_make_line_chart(start_date, end_date, value):
  """
      start_date: The start date chosen by the user via dash callback
      end_dte: The end date chosen by the user via dash callback

      Returns: Plotly graph object
  """
  value = [value] if type(value) != list else value
  line_chart_data = d.get_avg_price_by_month_and_make(start_date, end_date, value)
  return dash.dcc.Graph(
  id = 'avg_price_by_make_line_chart',
  figure = px.line(
      line_chart_data,
      x='inventory_month',
      y='price',
      color='make',
      title="Average Inventory Price by Month & Make",
      labels={ # replaces default labels by column name
          "inventory_month": "Inventory Month", "price": "Avg Inventory Price", 'make': 'Make'
      }
  )
)

##################################################
# Avg Mileage by Month & Make Line Chart
##################################################

@app.callback(
  Output('avg_mileage_by_make_line_chart', 'children'),
  Input('date-picker-range', 'start_date'),
  Input('date-picker-range', 'end_date'),
  Input('make-dropdown', 'value')
)
def make_avg_mileage_by_make_line_chart(start_date, end_date, value):
  """
  Returns a line chart of avg mileage by month and vehicle make

  :param start_date: The start date chosen by the user via dash callback
  :type start_date: str
  :param end_date: The end date chosen by the user via dash callback
  :type end_date: str
  :param value: The vehicle make chosen by the user via dash callback
  :type value: list

  :returns: a line chart of avg mileage by month and vehicle make
  :rtype: Dash graph object
  """
  value = [value] if type(value) != list else value
  line_chart_data = d.get_avg_mileage_by_month_and_make(start_date, end_date, value)
  return dash.dcc.Graph(
    id = 'avg_mileage_by_make_line_chart',
    figure = px.line(
        line_chart_data,
        x='inventory_month',
        y='mileage',
        color='make',
        title="Average Inventory Mileage by Month & Make",
        labels={ # replaces default labels by column name
            "inventory_month": "Inventory Month", "mileage": "Avg Inventory Mileage", 'make': 'Make'
        }
    )
  )

##################################################
# Avg Vehicle Year by Month & Make Line Chart
##################################################

@app.callback(
  Output('avg_vehicle_year_by_make_line_chart', 'children'),
  Input('date-picker-range', 'start_date'),
  Input('date-picker-range', 'end_date'),
  Input('make-dropdown', 'value')
)
def make_avg_vehicle_year_by_make_line_chart(start_date, end_date, value):
  """
  Returns a line chart of avg vehicle year by month and vehicle make

  :param start_date: The start date chosen by the user via dash callback
  :type start_date: str
  :param end_date: The end date chosen by the user via dash callback
  :type end_date: str
  :param value: The vehicle make chosen by the user via dash callback
  :type value: list

  :returns: a line chart of avg vehicle year by month and vehicle make
  :rtype: Dash graph object
  """
  value = [value] if type(value) != list else value
  line_chart_data = d.get_avg_vehicle_year_by_month_and_make(start_date, end_date, value)
  return dash.dcc.Graph(
    id = 'avg_vehicle_year_by_make_line_chart',
    figure = px.line(
        line_chart_data,
        x='inventory_month',
        y='vehicle_year',
        color='make',
        title="Average Inventory Year by Month & Make",
        labels={ # replaces default labels by column name
            "inventory_month": "Inventory Month", "vehicle_year": "Avg Inventory Year", 'make': 'Make'
        }
    )
  )

##################################################
## Data Table Vehicle Make Model Trim
##################################################

@app.callback(
  Output(component_id = 'make_model_trim_data', component_property = 'children'),
  Input('date-picker-range', 'start_date'),
  Input('date-picker-range', 'end_date'),
  Input('make-dropdown', 'value')
)
def make_data_table_vehicle_make(start_date, end_date, value):
  """
  Returns data table of vehicle makes

  :param start_date: The start date chosen by the user via dash callback
  :type start_date: str
  :param end_date: The end date chosen by the user via dash callback
  :type end_date: str

  :returns: Data table aggregated by vehicle makes
  :rtype: Dash graph object
  """
  value = [value] if type(value) != list else value
  data = d.get_make_model_trim_data(start_date, end_date, value)
  return dash.dash_table.DataTable(
    id='datatable-make-model-trim',
    columns=[
        {"name": i.title().replace('_', ' '), "id": i} for i in data.columns
    ],
    data = data.to_dict('records'),
    # editable = True,
    filter_action = "native",
    sort_action = "native",
    sort_mode = "multi",
    column_selectable="single",
    selected_columns=[],
    selected_rows=[],
    page_action="native",
    page_current= 0,
    page_size= 20,
  )



##################################################
## Collapse Filter
##################################################

filter_content = dash.html.Div([
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
  ], className="filter-section")

hide_filter = collapse.Collapse('hide_filter_make_detail', filter_content)
@app.callback(
  Output("hide_filter_make_detail", "is_open"),
  [Input("filter-collapse", "n_clicks")],
  [State("hide_filter_make_detail", "is_open")],
)
def toggle_collapse(filter_collapse, is_open):
  if filter_collapse:
    return not is_open
  return is_open


##################################################
## Collapse Info
##################################################

info = info_card.InfoCard(
  """
    Data has been aggregated from scraping 15 different dealership sites.

    Note that in May no data was scraped.
  """
)

hide_info = collapse.Collapse('hide_info_vehicle_detail', info)
@app.callback(
  Output("hide_info_vehicle_detail", "is_open"),
  [Input("info-collapse", "n_clicks")],
  [State("hide_info_vehicle_detail", "is_open")],
)
def toggle_collapse(info_collapse, is_open):
  if info_collapse:
    return not is_open
  return is_open


##################################################
## Pass Info to Header Component
##################################################

filter_button = dbc.Button(
  id="filter-collapse",
  className="fa-solid fa-filter",
  color="primary",
  n_clicks=0,
)
info_button = dbc.Button(
  id="info-collapse",
  className="fa-solid fa-info",
  color="primary",
  n_clicks=0,
)
header_props = {
  'title': 'Vehicle Make Details',
  'buttons': [filter_button, info_button],
  'collapsed_divs': [hide_filter, hide_info]
}
header = page_header.PageHeader(header_props)


##################################################
## Main Layout
##################################################

# Define the page layout
layout = dash.html.Div([
  # Header section
  header,

  # Main Dashboard Section
  dbc.Container([
    separator.Separator("At a Glance"),
    dash.html.Div(id="avg_price_by_make_line_chart", children=[]),
    dash.html.Div(id="avg_mileage_by_make_line_chart", children=[]),
    dash.html.Div(id="avg_vehicle_year_by_make_line_chart", children = []),

    separator.Separator("Detailed Make Model Trim Breakdown"),
    dash.html.Div(id="make_model_trim_data", children = []),
  ])

])
