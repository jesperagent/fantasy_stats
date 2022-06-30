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

grouped_data = data.groupby(['first_name','last_name', 'team_name'])[['minutes', 'xGoals', 'xAssists', 'xGI', 'goals',
                                                                      'assists', 'shots', 'key_passes', 'corners',
                                                                      'def_act']].sum()
grouped_data = grouped_data.reset_index()
grouped_data[['xGoals', 'xAssists', 'xGI']] = grouped_data[['xGoals', 'xAssists', 'xGI']].round(decimals = 2)

latest_gw = data['match_round'].max()
l5 = data.loc[(data['match_round'] >= (latest_gw-5)) & (data['match_round'] <= latest_gw)]
last_5 = l5.groupby(['first_name','last_name', 'team_name'])[['minutes', 'xGoals','xAssists', 'xGI', 'goals', 'assists',
                                                              'shots', 'key_passes', 'corners', 'def_act']].sum()
last_5 = last_5.reset_index()
last_5[['xGoals', 'xAssists', 'xGI']] = last_5[['xGoals', 'xAssists', 'xGI']].round(decimals = 2)

#-----------------------------------------------------------------------------------------------------------------------

#PAGE 1-----------------------------------------------------------------------------------------------------------------

table_tot = dash_table.DataTable(
    id='datatable_tot',
    data=grouped_data.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in grouped_data.columns],
    page_size=20,
    sort_action='native',
    cell_selectable=False,
    style_cell={'font-family':'sans-serif','textAlign': 'right'},
    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['first_name', 'last_name', 'team_name']
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

table_l5 = dash_table.DataTable(
    id='datatable_l5',
    data=last_5.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in grouped_data.columns],
    page_size=20,
    sort_action='native',
    cell_selectable=False,
    style_cell={'font-family':'sans-serif','textAlign': 'right'},
    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['first_name', 'last_name', 'team_name']
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

table_bgw = dash_table.DataTable(
    id='datatable_bgw',
    data=data.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in data.columns],
    page_size=20,
    sort_action='native',
    cell_selectable=False,
    style_cell={'font-family':'sans-serif','textAlign': 'right'},
    style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['first_name', 'last_name', 'team_name']
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

dropdown_bgw = html.Div(
    [
        dcc.Dropdown(
                    id='dropdown_bgw',
                    options=[{'label':i, 'value':i} for i in data['match_round'].unique()],
                    value=None,
                    placeholder='Select gameweek...'
        ),
        dcc.Dropdown(
                    id='dropdown_bgw2',
                    options=[{'label':i, 'value':i} for i in data['last_name'].unique()],
                    value=None,
                    placeholder='Select player...'
        ),
        dcc.Dropdown(
                    id='dropdown_bgw3',
                    options=[{'label': i, 'value': i} for i in sorted(data['team_name'].unique())],
                    value=None,
                    placeholder='Select team...'
        )
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

accordion = html.Div(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    table_tot
                ],
                title="Total",
            ),
            dbc.AccordionItem(
                [
                    table_l5
                ],
                title="Last 5 gws",
            ),
            dbc.AccordionItem(
                [
                    dropdown_bgw,
                    table_bgw
                ],
                title="By Gameweek",
             ),

        ],
        start_collapsed=True
    ))
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
            brand="Allsvenskan analytics",
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
            accordion
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

@app.callback(Output("datatable_bgw", "data"), [Input("dropdown_bgw", "value"), Input("dropdown_bgw2", "value"),
                                            Input("dropdown_bgw3", "value")])
def update_datatable_bgw(d1, d2, d3):
    if (d1 != None and d2 != None and d3 != None):
        filtered_df = data[(data["match_round"] == d1) & (data["last_name"] == d2) & (data["team_name"] == d3)]
        return filtered_df.to_dict("records")
    if (d1 != None and d2 != None and d3 == None):
        filtered_df = data[(data["match_round"] == d1) & (data["last_name"] == d2)]
        return filtered_df.to_dict("records")
    if (d1 != None and d2 == None and d3 != None):
        filtered_df = data[(data["match_round"] == d1) & (data["team_name"] == d3)]
        return filtered_df.to_dict("records")
    if (d1 == None and d2 != None and d3 != None):
        filtered_df = data[(data["last_name"] == d2) & (data["team_name"] == d3)]
        return filtered_df.to_dict("records")
    if (d1 != None and d2 == None and d3 == None):
        filtered_df = data[data['match_round'] == d1]
        return filtered_df.to_dict("records")
    if (d1 == None and d2 != None and d3 == None):
        filtered_df = data[data['last_name'] == d2]
        return filtered_df.to_dict("records")
    if (d1 == None and d2 == None and d3 != None):
        filtered_df = data[data['team_name'] == d3]
        return filtered_df.to_dict("records")
    else:
        filtered_df = data
        return filtered_df.to_dict("records")
#-----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run_server(debug=True)
