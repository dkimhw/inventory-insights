# Import necessary libraries
import dash
import dash_bootstrap_components as dbc


# Define the navbar structure
def TitleSection(title):
  layout = dash.html.Div([
    dash.html.H1(title, id="title-section")
  ])

  return layout
