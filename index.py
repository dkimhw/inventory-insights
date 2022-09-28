from dash import html, dcc
from dash.dependencies import Input, Output

# Connect to your app pages
from pages import home, make_detail

# Connect the navbar to the index
from components import navbar
from components import title_section
from app import app


# components
nav = navbar.Navbar()

app.layout = html.Div([
  dcc.Location(id='url', refresh=False),
  nav,
  html.Div(id='title-section', children=[]),
  html.Div(id='page-content', children=[]),
])
app.css.config.serve_locally = True

@app.callback(
  Output('page-content', 'children'),
  [Input('url', 'pathname')]
)
def display_page(pathname):
  if pathname == '/':
      return home.layout
  if pathname == '/make-detail':
      return make_detail.layout

if __name__ == '__main__':
    app.run_server(debug=True)
