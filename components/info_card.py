import dash_bootstrap_components as dbc
import dash

def InfoCard(content = ''):
  layout = dash.html.Div(
    dash.html.Div(
      dash.html.Div(content),
      className='info-card'
    ),
  )

  return layout
