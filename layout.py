from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

# Load data
data = pd.read_parquet('data/house_price_data_20-05-2024.parquet')

# Get unique values for dropdowns
municipalities = data['municipality'].unique()
garages = data['garage'].unique()
home_types = data['home_type'].unique()
home_sizes = data['home_size'].unique()
elevators = data['elevator'].unique()

sidebar = dbc.Col(
    [
        html.H2("Filters", className="display-4"),
        html.Hr(),
        html.P("Select filters to refine the data", className="lead"),
        html.Label('Municipality'),
        dcc.Dropdown(
            id='municipality-dropdown',
            options=[{'label': municipality, 'value': municipality} for municipality in municipalities],
            placeholder='Select Municipality'
        ),
        html.Label('Parish'),
        dcc.Dropdown(
            id='parish-dropdown',
            placeholder='Select Parish'
        ),
        html.Label('Home Type'),
        dcc.Dropdown(
            id='home_type-dropdown',
            options=[{'label': home_type, 'value': home_type} for home_type in home_types],
            placeholder='Select Home Type'
        ),
        html.Label('Home Size'),
        dcc.Dropdown(
            id='home_size-dropdown',
            options=[{'label': home_size, 'value': home_size} for home_size in home_sizes],
            placeholder='Select Home Size'
        ),
        html.Button('Apply Filters', id='apply-filters-button', n_clicks=0, className='mt-2')
    ],
    width=3,
    style={"position": "fixed", "top": 0, "left": 0, "bottom": 0, "padding": "2rem 1rem", "background-color": "#f8f9fa"}
)

content = dbc.Col(
    [
        html.H1('Rent Dashboard', 
                className='display-3'),
        html.Div(id='indicator-row', children=[
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-home me-2"), 
                            html.H5("Number of Listings", className="card-title", style={"display": "inline"})
                        ], style={"display": "flex", 
                                  "align-items": "center"}),
                        html.P(id='num-houses', 
                               className="card-text"),
                        html.Div(id='home-size-graph', className="card-text")
                    ])
                ], className="mb-4 d-flex text-center")), 
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-home me-2"), 
                            html.H5("Average Price", className="card-title", style={"display": "inline"})
                        ], style={"display": "flex", "align-items": "center"}),
                        html.P(id='avg-price', 
                               className="card-text"),
                        html.Div(id='avg-price-graph',
                                 className="card-text")
                    ])
                ], className="mb-4 d-flex text-center")),
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fa-solid fa-expand"), 
                            html.H5("Average Home Area", className="card-title", style={"display": "inline"})
                        ], style={"display": "flex", "align-items": "center"}),
                        html.P(id='avg-area', 
                               className="card-text"),
                        html.Div(id='avg-area-graph',
                                 className="card-text")
                    ])
                ], className="mb-4 d-flex text-center")),
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fa-solid fa-coins"), 
                            html.H5("Average Price per Square Meter", className="card-title", style={"display": "inline"})
                        ], style={"display": "flex", "align-items": "center"}),
                        html.P(id='avg-price-per-sqr-meter', 
                               className="card-text"),
                        html.Div(id='avg-price-per-sqr-meter-graph',
                                 className="card-text")
                    ])
                ], className="mb-4 d-flex text-center"))
            ])
        ]),
        html.Div(id='content-area'),
        html.Div([
            dcc.Graph(
                id='scatter-plot'
            ),
            html.Div(
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(
                            id='home-size-distribution',
                            style={"height": "35vh"}
                        ), 
                        width=2,
                    ),
                    dbc.Col(
                        dcc.Graph(
                            id='home-type-distribution',
                            style={"height": "35vh"}
                        ), 
                        width=2,
                    ),
                    dbc.Col(
                        dcc.Graph(
                            id='home-type-heatmap',
                            style={"height": "35vh"}
                        ), 
                        width=8,
                    )
                ]),
                className="mt-4"
            )
        ]),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Detailed Information")),
                dbc.ModalBody(id='popup-content'),
                dbc.ModalFooter(
                ),
            ],
            id="popup",
            is_open=False,
            centered=True,
            size = "xl"
        )
    ],
    width={"size": 9, "offset": 3},
    style={"padding": "2rem 1rem"}
)


layout = html.Div([sidebar, content])
