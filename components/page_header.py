# Import necessary libraries
import dash
import dash_bootstrap_components as dbc

# Define the navbar structure
def PageHeader(props):
  icon_container = []
  icon_container.append(dash.html.H1(f"{props['title']}", className="dashboard-title"))
  for button in props['buttons']:
    icon_container.append(button)

  collapsed_content = []
  for item in props['collapsed_divs']:
    collapsed_content.append(item)

  layout = dash.html.Div([
    dbc.Container([
      # Title & Filter Icons
      dash.html.Div(
        children = icon_container
      , className="icon-container"),

      # Collapsed Section
      dash.html.Div(
        children = collapsed_content
      )
    ])
  ], id="dashboard-title-section")

  return layout
