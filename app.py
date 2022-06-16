import dash
from dash import dash_table
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd

#-----------------------------------------------------------------------------------------------------------------------

app = dash.Dash(external_stylesheets=[dbc.themes.SLATE])

#-----------------------------------------------------------------------------------------------------------------------

data = pd.read_csv('fotmob_players.csv')

table_p1 = dash_table.DataTable(
    id='datatable',
    data=data.to_dict('records'),
    columns=[{'id': c, 'name': c, 'hideable':True} for c in data.columns],
    page_size=20,
    sort_action='native',
    cell_selectable=False,
    hidden_columns=['Unnamed: 0','id'],
    style_cell={'font-family':'sans-serif','textAlign': 'center'},
    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['first_name', 'second_name', 'team', 'position']
    ],
    style_table={'overflowX': 'auto'},
    style_as_list_view=True,
    style_data_conditional=[{
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    }],
    style_header_conditional=[{
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    }]
)

dropdown_p1 = html.Div(
    [
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem(
                    "Last 5 GWs", id="dropdown-button", n_clicks=0
                ),
                dbc.DropdownMenuItem(
                    "All GWs", id="dropdown-button2", n_clicks=0
                )
            ],
            label="Select GWs",
        ),
        html.P(id="item-clicks", className="mt-3"),
    ]
)

text_input = html.Div(
    [
        dbc.Input(id="input", placeholder="Enter your team ID...", type="text"),
        html.Br(),
        html.P(id="output")])

text_input2 = html.Div(
    [
        dbc.Input(id="input", placeholder="Enter your league ID...", type="text"),
        html.Br(),
        html.P(id="output")])
#-----------------------------------------------------------------------------------------------------------------------
app.layout = html.Div(
    [
        dcc.Location(id="url"),
        dbc.NavbarSimple(
            children=[
                dbc.NavLink("Stats from Fotmob", href="/", active="exact"),
                dbc.NavLink("Stats from Allsvenskan Fantasy", href="/page-1", active="exact"),
                dbc.NavLink("Stats from Twelve", href="/page-2", active="exact"),
            ],
            brand="Allsvenkan analytics",
            color="primary",
            dark=True,
        ),
        dbc.Container(id="page-content", className="pt-4"),
    ]
)

#-----------------------------------------------------------------------------------------------------------------------

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return [
            dropdown_p1,
            table_p1
        ]
    elif pathname == "/page-1":
        return [
            text_input2
        ]
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

@app.callback(
    Output("datatable", "data"),
    [Input("dropdown-button", "n_clicks")],
    [Input("dropdown-button2", "n_clicks")],
)
def count_clicks(*args):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = "all"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == 'dropdown-button':
        df = data.loc[data["Last"] == 'L5']
    elif button_id == 'dropdown-button2':
        df = data.loc[data["Last"] == 'All']
    else:
        df = pd.read_csv('fotmob_players.csv')

    return df.to_dict('records')

#-----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run_server(debug=True)
