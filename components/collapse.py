import dash_bootstrap_components as dbc
import dash

def Collapse(collapse_id, content = ''):
  layout = dbc.Row(
        dbc.Collapse(
          content,
          id=f"{collapse_id}",
          is_open=False,
        ),
      )

  return layout
