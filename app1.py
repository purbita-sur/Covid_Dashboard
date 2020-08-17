import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import covid_analysis

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

obj = covid_analysis.covid_analysis()

app.layout = html.Div(
    [
        dbc.Navbar(dbc.NavbarBrand('Covid-19 Dashboard'), dark=True, color='primary', style={'marginBottom': '1%'}),
        dbc.Row([dbc.Col(["World"

                          ])], style={'color':'blue','fontSize': 30, 'font-weight': 'bold', 'marginBottom': '2%'}),
        dbc.Row(
            [
                dbc.Col(dbc.Card([dbc.CardHeader("Confirmed", style={'fontSize': 30, 'font-weight': 'bold'}),
                                  dbc.CardBody(html.H5(id='WorldConfirmed', className="card-title"))], color="info",
                                 inverse=True)),
                dbc.Col(
                    dbc.Card([dbc.CardHeader("Recovered", style={'fontSize': 30, 'font-weight': 'bold'}),
                              dbc.CardBody(html.H5(id='WorldRecovered', className="card-title"))], color="success",
                             inverse=True)
                ),
                dbc.Col(dbc.Card([dbc.CardHeader("Deaths", style={'fontSize': 30, 'font-weight': 'bold'}),
                                  dbc.CardBody(html.H5(id='WorldDead', className="card-title"))], color="danger",
                                 inverse=True)),
            ],
            className="mb-4",
        ),
        dbc.Row([dbc.Col([
            html.H4("Covid Graph"),
            dcc.Graph(
                id='WorldGraph'
            )
        ])], style={'border': '1px solid black', 'marginBottom': '2%'}),
        dbc.Row([dbc.Col([
            html.H4("World Map for Covid active locations"),
            dcc.Graph(
                id='WorldMap'
            )
        ])], style={'border': '1px solid black', 'marginBottom': '2%'}),
        dbc.Row([dbc.Col(["India"
                          ])], style={'color':'blue','fontSize': 30, 'font-weight': 'bold', 'marginBottom': '2%'}),
        dbc.Row(
            [
                dbc.Col(dbc.Card([dbc.CardHeader("Confirmed", style={'fontSize': 30, 'font-weight': 'bold'}),
                                  dbc.CardBody(html.H5(id='IndiaConfirmed', className="card-title"))], color="info",
                                 inverse=True))
            ],
            className="mb-4",
        ),
        dbc.Row([dbc.Col(html.H4('Top 10 Covid Positive States'))]),
        dbc.Row([dbc.Col(id='CovidStates')], style={'marginBottom': '2%'}),
        dbc.Row([dbc.Col(html.H4('Top 10 States according to number of tests conducted so far'))]),
        dbc.Row([dbc.Col(id='CovidTests')], style={'marginBottom': '2%'}),
        dcc.Interval(
            id='interval-component',
            interval=360 * 1000,  # in milliseconds
            n_intervals=0
        )
    ])


@app.callback(
    [Output('WorldConfirmed', 'children'),
     Output('WorldRecovered', 'children'),
     Output('WorldDead', 'children')],
    [Input('interval-component', 'n_intervals')])
def update_info(n):
    cases = obj.count_covid_cases()
    return cases[0], cases[1], cases[2]

@app.callback(
    Output('WorldGraph', 'figure'),
    [Input('interval-component', 'n_intervals')])
def update_graph(n):
    cov_graph = obj.world_graph()
    data = [go.Scatter(x=cov_graph[0], y=cov_graph[1], mode='markers+lines')]
    layout = go.Layout(xaxis={'title': 'Dates'}, yaxis={'title': 'Number of Cases'},hovermode='closest')
    return {'data': data, 'layout': layout}

@app.callback(
    Output('WorldMap', 'figure'),
    [Input('interval-component', 'n_intervals')])
def update_map(n):
    df = obj.world_active
    s = df.columns[-1]
    new_s = 'Cases till ' + s
    df = df.rename(columns={s: new_s})
    size=df.columns[-1]
    fig = px.scatter_geo(df, lat='Lat', lon='Long', color=size, hover_name="Country/Region",
                         color_continuous_scale=px.colors.sequential.Plasma, range_color=[0, 100])
    return fig

@app.callback(
    Output('IndiaConfirmed', 'children'),
    [Input('interval-component', 'n_intervals')])
def update_ind_info(n):
    ind_total = obj.ind_count()
    return ind_total

@app.callback(
    Output('CovidStates', 'children'),
    [Input('interval-component', 'n_intervals')])
def update_covid_states(n):
    covid_top = obj.covid_top_cases()
    return dbc.Table.from_dataframe(covid_top, striped=True, bordered=True, hover=True,className='table-danger')

@app.callback(
    Output('CovidTests', 'children'),
    [Input('interval-component', 'n_intervals')])
def update_covid_states(n):
    covid_test = obj.covid_total_tested()
    return dbc.Table.from_dataframe(covid_test, striped=True, bordered=True, hover=True,className='table-success')

if __name__ == '__main__':
    app.run_server(debug=True)
