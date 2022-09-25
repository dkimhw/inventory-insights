# Import necessary libraries
import dash
import dash_bootstrap_components as dbc

# Define the navbar structure
def Separator(title):
  layout = dash.html.Div([
    dash.html.H2(title, className="separator")
  ])

  return layout
