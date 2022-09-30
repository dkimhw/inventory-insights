
import dash
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import services.summary_data as d
import plotly.express as px
from dash import dcc, Input, Output
from datetime import date
import dash_bootstrap_components as dbc
import datetime
from app import app
from components import collapse, separator, page_header, info_card

##################################################
# Starting Variables
##################################################

end_date =  datetime.date.today()
start_date = datetime.date(end_date.year, end_date.month - 5, 1).strftime("%Y-%m-%d")
end_date = end_date.strftime("%Y-%m-%d")

indicator_chart_height = 200
indicator_font_size = 32

##################################################
# Tile: Average Inventory Price
##################################################

# Creates a graph object that displays avg car price based on last scraped month
@app.callback(
  Output(component_id = 'avg_inventory_price', component_property = 'children'),
  Input('date-picker', 'start_date'),
  Input('date-picker', 'end_date')
)
def make_avg_price_indicator_chart (start_date, end_date):
  """
      start_date: The start date chosen by the user via dash callback
      end_dte: The end date chosen by the user via dash callback

      Returns: Plotly graph object
  """
  price = d.avg_inventory_price(start_date, end_date)
  return dcc.Graph(
    figure = {
      'data': [
        go.Indicator(
          mode = "number",
          value = price,
          number={"font":{"size": indicator_font_size}},
        )
      ],
      'layout': go.Layout(
        title = 'Average Inventory Price',
        height = indicator_chart_height,
      )
    }
  )

##################################################
# Tile: Average Inventory Year
##################################################

@app.callback(
    Output('avg_inventory_make_year', 'children'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)
def make_avg_make_year_chart (start_date, end_date):
  """
      start_date: The start date chosen by the user via dash callback
      end_dte: The end date chosen by the user via dash callback

      Returns: Plotly graph object
  """
  avg_year = d.avg_vehicle_year(start_date, end_date)
  return dcc.Graph(
    figure = {
      'data': [
        go.Indicator(
          mode = "number",
          value = avg_year,
          number={"font":{"size": indicator_font_size}, 'valueformat':'f'},
        )
      ],
      'layout': go.Layout(
          title = 'Average Inventory Make Year',
          height = indicator_chart_height
      )
    }
  )

##################################################
# Tile: Average Inventory Mileage
##################################################

@app.callback(
    Output(component_id = 'avg_inventory_mileage', component_property = 'children'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)
def make_avg_inventory_mileage (start_date, end_date):
  """
      start_date: The start date chosen by the user via dash callback
      end_dte: The end date chosen by the user via dash callback

      Returns: Plotly graph object
  """
  avg_mileage = d.avg_vehicle_mileage(start_date, end_date)
  return dcc.Graph(
    figure = {
      'data': [
        go.Indicator(
          mode = "number",
          value = avg_mileage,
          number={"font":{"size": indicator_font_size}},
        )
      ],
      'layout': go.Layout(
        title = 'Average Inventory Mileage',
        height = indicator_chart_height
      )
    }
  )

##################################################
# Count of Makes Bar Chart
##################################################

@app.callback(
    Output('make_count_bar_chart', 'children'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)
def make_bar_chart (start_date, end_date):
  """
      start_date: The start date chosen by the user via dash callback
      end_dte: The end date chosen by the user via dash callback

      Returns: Plotly graph object
  """
  makes_data = d.make_count(start_date, end_date)
  return dcc.Graph(figure = px.bar(
    makes_data,
    y='vin',
    x='make',
    text_auto='.2s',
    title="Count of Used Cars by Make",
    labels={ # replaces default labels by column name
        "vin": "Count of Vehicles", "make": "Make"
    }
  ))


##################################################
# Avg Price by Month Line Chart
##################################################

@app.callback(
    Output('avg_price_line_chart', 'children'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)
def make_avg_price_line_chart(start_date, end_date):
  """
    start_date: The start date chosen by the user via dash callback
    end_dte: The end date chosen by the user via dash callback

    Returns: Plotly graph object
  """
  line_chart_data = d.avg_price_by_month(start_date, end_date)
  return dcc.Graph(figure = px.line(
      line_chart_data,
      x='inventory_month',
      y='price',
      title="Average Inventory Price by Month",
      labels={ # replaces default labels by column name
          "inventory_month": "Inventory Month", "price": "Avg Inventory Price"
      }
  ))

##################################################
# Avg Mileage by Month Line Chart
##################################################

@app.callback(
    Output('avg_mileage_line_chart', 'children'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)
def make_avg_mileage_line_chart(start_date, end_date):
  """
  Returns a line chart of average mileage by month

  :params start_date: The start date used to display specific time range for the line chart
  :type start_date: str
  :params end_date: The end date used to display specific time range for the line chart
  :type end_date: str

  :returns: Dash graph object of average mileage by month
  :rtype: Dash graph object
  """
  line_chart_data = d.avg_mileage_by_month(start_date, end_date)
  return dcc.Graph(figure = px.line(
      line_chart_data,
      x='inventory_month',
      y='avg_mileage',
      title="Average Inventory Mileage by Month",
      labels={ # replaces default labels by column name
          "inventory_month": "Inventory Month", "avg_mileage": "Avg Inventory Mileage"
      }
  ))


##################################################
# Avg Delaership Inventory Size by Month Line Chart
##################################################

@app.callback(
  Output(component_id = 'avg_dealership_inventory_size_by_month_line_chart', component_property = 'children'),
  Input('date-picker', 'start_date'),
  Input('date-picker', 'end_date')
)
def make_avg_dealership_inventory_size_line_chart(start_date, end_date):
  """
      start_date: The start date chosen by the user via dash callback
      end_dte: The end date chosen by the user via dash callback

      Returns: Plotly graph object
  """
  line_chart_data = d.avg_dealership_inventory_size_by_month(start_date, end_date)
  return dcc.Graph(
    figure = px.line(
        line_chart_data,
        x='inventory_month',
        y='inventory_size',
        title="Average Dealership Inventory Size by Month",
        labels={ # replaces default labels by column name
            "inventory_month": "Inventory Month", "inventory_size": "Average Inventory Size per Dealership"
        }
    )
  )

##################################################
# Transmission Type Count Bar Chart
##################################################


@app.callback(
  Output(component_id = 'transmission_bar_chart', component_property = 'children'),
  Input('date-picker', 'start_date'),
  Input('date-picker', 'end_date')
)
def make_transmission_bar_chart (start_date, end_date):
  """
      start_date: The start date chosen by the user via dash callback
      end_dte: The end date chosen by the user via dash callback

      Returns: Plotly graph object
  """
  data = d.transmission_type_count(start_date, end_date)
  return dcc.Graph(
    figure = px.bar(
        data,
        y='count_of_vehicles',
        x='transmission',
        text_auto='.2s',
        title="Count of Used Cars by Transmission",
        labels={ # replaces default labels by column name
            "count_of_vehicles": "Count of Vehicles", "transmission": "Transmission Type"
        }
    )
  )

##################################################
# Drivetrain Type Count Bar Chart
##################################################

@app.callback(
  Output(component_id = 'drivetrain_bar_chart', component_property = 'children'),
  Input('date-picker', 'start_date'),
  Input('date-picker', 'end_date')
)
def make_drivetrain_bar_chart (start_date, end_date):
  """
      start_date: The start date chosen by the user via dash callback
      end_dte: The end date chosen by the user via dash callback

      Returns: Plotly graph object
  """
  data = d.drivetrain_type_count(start_date, end_date)
  return dcc.Graph(
    figure = px.bar(
        data,
        y='count_of_vehicles',
        x='drivetrain',
        text_auto='.2s',
        title="Count of Used Cars by Drivetrain",
        labels={ # replaces default labels by column name
            "count_of_vehicles": "Count of Vehicles", "drivetrain": "Drivetrain Type"
        }
    )
  )

##################################################
# Exterior Color Type Count Bar Chart
##################################################

@app.callback(
  Output(component_id = 'exterior_color_bar_chart', component_property = 'children'),
  Input('date-picker', 'start_date'),
  Input('date-picker', 'end_date')
)
def make_exterior_color_bar_chart (start_date, end_date):
  """
      start_date: The start date chosen by the user via dash callback
      end_dte: The end date chosen by the user via dash callback

      Returns: Plotly graph object
  """
  data = d.exterior_color_type_count(start_date, end_date)
  return dcc.Graph(
    figure = px.bar(
        data,
        y='count_of_vehicles',
        x='exterior_color',
        text_auto='.2s',
        title="Count of Used Cars by Exterior Color",
        labels={ # replaces default labels by column name
            "count_of_vehicles": "Count of Vehicles", "exterior_color": "Exterior Color"
        }
    )
  )

##################################################
# Count of Makes by Month Line Chart
##################################################

@app.callback(
    Output(component_id = 'count_of_vehicles_by_makes_and_month', component_property = 'children'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)
def make_make_month_line_chart(start_date, end_date):
  """
      start_date: The start date chosen by the user via dash callback
      end_dte: The end date chosen by the user via dash callback

      Returns: Plotly graph object
  """
  data = d.make_count_by_month(start_date, end_date)
  return dcc.Graph(
    figure = px.line(
      data,
      y='count_of_vehicles',
      x='inventory_month',
      color="make",
      title="Count of Used Cars by Inventory Month & Make (Top 10 Makes Only)",
      labels={ # replaces default labels by column name
          "vin": "Count of Vehicles", "inventory_month": "Inventory Month"
      }
    )
  )


##################################################
# Vehicle Year Histogram
##################################################

@app.callback(
    Output(component_id = 'count_of_vehicles_by_vehicle_year', component_property = 'children'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)
def make_vehicle_year_bar_chart (start_date, end_date):
  """
    start_date: The start date chosen by the user via dash callback
    end_dte: The end date chosen by the user via dash callback

    Returns: Plotly graph object
  """
  data = d.vehicle_year_count(start_date, end_date)
  fig = px.histogram(
    data,
    y='count_of_vehicles',
    x='year',
    marginal='box',
    text_auto='.2s',
    histfunc='sum',
    title="Vehicle Year Frequency Chart",
    labels={
        "year": "Vehicle Year",
        "count_of_vehicles": "Count of Vehicles"
    },
    nbins= 20,
    color_discrete_sequence=['#4C6793']
  ).update_layout(
    yaxis_title="Count of Vehicles"
  )
  return dcc.Graph(
    figure = fig
  )

##################################################
# Mileage Histogram
##################################################

@app.callback(
    Output(component_id = 'mileage_distribution_chart', component_property = 'children'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)
def make_mileage_distribution_chart (start_date, end_date):
  """
    start_date: The start date chosen by the user via dash callback
    end_dte: The end date chosen by the user via dash callback

    Returns: Plotly graph object
  """
  data = d.get_mileage_distribution_data(start_date, end_date)
  fig = px.histogram(
    data,
    y='count_of_vehicles',
    x='mileage',
    marginal="box",
    text_auto='.2s',
    histfunc='sum',
    title="Vehicle Mileage Frequency Chart",
    labels={ # replaces default labels by column name
      "mileage": "Mileage"
    },
    color_discrete_sequence=['#4C6793']
  ).update_layout(
    yaxis_title="Count of Vehicles"
  )
  return dcc.Graph(
    figure = fig

  )

##################################################
# Price Histogram
##################################################

@app.callback(
    Output(component_id = 'price_distribution_chart', component_property = 'children'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)
def make_price_distribution_chart (start_date, end_date):
  """
    start_date: The start date chosen by the user via dash callback
    end_dte: The end date chosen by the user via dash callback

    Returns: Plotly graph object
  """
  data = d.get_price_distribution_data(start_date, end_date)
  fig = px.histogram(
    data,
    y='count_of_vehicles',
    x='price',
    marginal="box",
    text_auto='.2s',
    histfunc='sum',
    title="Vehicle Price Frequency Chart",
    labels={ # replaces default labels by column name
      "price": "Price"
    },
    nbins=30,
    color_discrete_sequence=['#4C6793']
  ).update_layout(
    yaxis_title="Count of Vehicles"
  )
  return dcc.Graph(
    figure = fig
  )

##################################################
# Make Data Table
##################################################

headerColor = 'grey'
rowEvenColor = 'lightgrey'
rowOddColor = 'white'

@app.callback(
  Output(component_id = 'make_data_table', component_property = 'children'),
  Input('date-picker', 'start_date'),
  Input('date-picker', 'end_date')
)
def make_data_table_vehicle_make(start_date, end_date):
  """
  Returns data table of vehicle makes

  :param start_date: The start date chosen by the user via dash callback
  :type start_date: str
  :param end_date: The end date chosen by the user via dash callback
  :type end_date: str

  :returns: Data table aggregated by vehicle makes
  :rtype: Dash graph object
  """
  data = d.get_make_table_data(start_date, end_date)
  return dash.dash_table.DataTable(
    id='datatable-interactivity',
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
    page_size= 10,
  )

##################################################
## Collapse Filter
##################################################

filter_content = dbc.Row(
  dcc.DatePickerRange(
    id='date-picker',
    min_date_allowed=date(2022, 1, 1),
    initial_visible_month=start_date,
    start_date=start_date,
    end_date=end_date
  )
)

hide_filter = collapse.Collapse('hide_filter', filter_content)
@app.callback(
  Output("hide_filter", "is_open"),
  [Input("filter-collapse", "n_clicks")],
  [State("hide_filter", "is_open")],
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

hide_info = collapse.Collapse('hide_info', info)
@app.callback(
  Output("hide_info", "is_open"),
  [Input("info-collapse", "n_clicks")],
  [State("hide_info", "is_open")],
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
  'title': 'Summary',
  'buttons': [filter_button, info_button],
  'collapsed_divs': [hide_filter, hide_info]
}
header = page_header.PageHeader(header_props)

##################################################
## Main Layout
##################################################

layout = dash.html.Div([
  # Header section
  header,

  # Main section
  dbc.Container([
    # Dashboard Body
    # At a Glance Section
    separator.Separator("At a Glance"),
    dash.html.Div(id="indicators", children = [
      dash.html.Div(id="avg_inventory_price", children = [], className="indicator-chart"),
      dash.html.Div(id="avg_inventory_make_year", children = [], className="indicator-chart"),
      dash.html.Div(id="avg_inventory_mileage", children = [], className="indicator-chart")
    ], className="indicator-chart-section"),
    dash.html.Div(id="avg_price_line_chart", children = []),
    dash.html.Div(id="avg_mileage_line_chart", children = []),
    dash.html.Div(id="avg_dealership_inventory_size_by_month_line_chart", children = []),

    # Create a distribution section for year, price, and mileage
    separator.Separator("Distribution of Vehicle Year, Price, and Mileage"),
    dash.html.Div(id="count_of_vehicles_by_vehicle_year", children = []),
    dash.html.Div(id="mileage_distribution_chart", children = []),
    dash.html.Div(id="price_distribution_chart", children = []),

    # Additional Vehicle Information Section
    separator.Separator("Additional Vehicle Information"),
    dash.html.Div(id="make_count_bar_chart", children = []),
    dash.html.Div(id="count_of_vehicles_by_makes_and_month", children = []),
    dash.html.Div(id="transmission_bar_chart", children = []),
    dash.html.Div(id="drivetrain_bar_chart", children = []),
    dash.html.Div(id="exterior_color_bar_chart", children = []),

    # Make overview data table
    separator.Separator("Detailed Vehicle Make Overview"),
    dash.html.Div(id="make_data_table", children = [], className="mt-4 mb-4")
  ])
])
