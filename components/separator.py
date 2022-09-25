# Import necessary libraries
import dash
import dash_bootstrap_components as dbc

# Define the navbar structure
def Separator():
  layout = dash.html.Div([
    dbc.NavbarSimple(
      children=[
          dbc.NavItem(dbc.NavLink("Summary", href="/"), className="navbar-links-styles"),
          dbc.NavItem(dbc.NavLink("Make Detail", href="/make-detail"), className="navbar-links-styles"),
      ] ,
      brand="Inventory Insights",
      brand_href="/",
      color="dark",
      dark=True,
      className="navbar-brand-styles"
    ),
  ])

  return layout
