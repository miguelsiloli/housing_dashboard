from dash import Dash
import dash_bootstrap_components as dbc
from layout import layout
from dash import Input, Output, State
import pandas as pd
from dash import html, dcc
import plotly.express as px
import plotly.figure_factory as ff

# Load data
data = pd.read_parquet('data/house_price_data_20-05-2024.parquet')

app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP, 
                                 dbc.icons.FONT_AWESOME])

@app.callback(
    Output('parish-dropdown', 'options'),
    [Input('municipality-dropdown', 'value')]
)
def update_parish_options(selected_municipality):
    if selected_municipality is None:
        return []
    parishes = data[data['municipality'] == selected_municipality]['parish'].unique()
    return [{'label': parish, 'value': parish} for parish in parishes]

"""
@app.callback(
    Output('neighborhood-dropdown', 'options'),
    [Input('parish-dropdown', 'value')],
    [State('municipality-dropdown', 'value')]
)
def update_neighborhood_options(selected_parish, selected_municipality):
    if selected_parish is None or selected_municipality is None:
        return []
    neighborhoods = data[(data['municipality'] == selected_municipality) & (data['parish'] == selected_parish)]['neighborhood'].unique()
    return [{'label': neighborhood, 'value': neighborhood} for neighborhood in neighborhoods]
"""

@app.callback(
    [
        Output('num-houses', 'children'),
        Output('avg-price', 'children'),
        Output('avg-area', 'children'),
        Output('avg-price-per-sqr-meter', 'children'),
        Output('scatter-plot', 'figure'),        
        Output('avg-price-graph', 'figure'),
        Output('avg-area-graph', 'figure'),
        Output('avg-price-per-sqr-meter-graph', 'figure'),
        Output('home-size-graph', 'figure'),
        Output('home-size-distribution', 'figure'),
        Output('home-type-distribution', 'figure'),
        Output('home-type-heatmap', 'figure')
    ],
    [Input('apply-filters-button', 'n_clicks')],
    [
        State('municipality-dropdown', 'value'),
        State('parish-dropdown', 'value'),
        State('home_type-dropdown', 'value'),
        State('home_size-dropdown', 'value'),
    ]
)
def apply_filters(n_clicks, municipality, parish, home_type, home_size):
    if n_clicks is None:
        n_clicks = 0

    if n_clicks == 0:
        # initial call no filter
        filtered_data = data.copy()
    else:
        # filter
        filtered_data = data.copy()

        if municipality:
            filtered_data = filtered_data[filtered_data['municipality'] == municipality]
        if parish:
            filtered_data = filtered_data[filtered_data['parish'] == parish]
        if home_type:
            filtered_data = filtered_data[filtered_data['home_type'] == home_type]
        if home_size:
            filtered_data = filtered_data[filtered_data['home_size'] == home_size]

    num_houses = len(filtered_data)
    avg_price = filtered_data['price'].mean()
    avg_area = filtered_data['home_area'].mean()
    avg_price_per_sqr_meter = (filtered_data['price'] / filtered_data['home_area']).mean()

    aggregated_data = filtered_data.groupby('parish', as_index=False).agg({
        'price': ['sum', 'mean'],
        'home_area': 'mean',
        'price_per_sqr_meter': 'mean',
        'municipality': 'first'
    })
    aggregated_data.columns = ['parish', 'total_price', 'avg_price', 'avg_home_area', 'price_per_sqr_meter', 'municipality']

    bubble_chart = px.scatter(aggregated_data, 
                              x='avg_price', 
                              y='avg_home_area', 
                              size='total_price',
                              color='municipality', 
                              hover_name='parish', 
                              log_x=False, 
                              size_max=60)

    bubble_chart.update_traces(
        hovertemplate=(
            "Municipality: %{customdata[0]}<br>"
            "Parish: %{customdata[1]}<br>"
            "Average Home Area: %{y:.2f} m²<br>"
            "Average Price: %{x:.2f} €<br>"
            "Total Volume: %{marker.size:,} €<br>"
            "Average Price per Square Meter: %{customdata[2]:.2f} €/m²<br>"
            "<extra></extra>"
        ),
        customdata=aggregated_data[['municipality', 'parish', 'price_per_sqr_meter']].values
    )

    bubble_chart.update_layout(
        xaxis_title="Average Price",
        yaxis_title="Home Area",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    avg_price_by_home_size = filtered_data.groupby('home_size')['price'].mean().reset_index()
    home_size_barchart = px.bar(avg_price_by_home_size, 
                                x='price', 
                                y='home_size', 
                                # title='Average Price by Home Size',
                                orientation= "h")   

    home_size_barchart.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title=""),
        yaxis=dict(title=""),
    )

    avg_price_by_home_type = filtered_data.groupby('home_type')['price'].mean().reset_index()
    home_type_barchart = px.bar(avg_price_by_home_type, 
                                x='price', 
                                y='home_type', 
                                # title='Average Price by Home Type',
                                orientation= "h")   

    home_type_barchart.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(title=""),
        yaxis=dict(title=""),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    price_kdeplot = ff.create_distplot([filtered_data["price"]], 
                                       group_labels=["price"],
                                       curve_type="kde", 
                                       show_hist=False,
                                       show_rug=False,
                                       bin_size=.2)

    price_kdeplot.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showticklabels=False, title=""),
        yaxis=dict(showticklabels=False, title=""),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )

    area_kdeplot = ff.create_distplot([filtered_data["home_area"]], 
                                       group_labels=["home_area"],
                                       curve_type="kde", 
                                       show_hist=False,
                                       show_rug=False,
                                       bin_size=.2)

    area_kdeplot.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showticklabels=False, title=""),
        yaxis=dict(showticklabels=False, title=""),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )

    price_per_sqr_meter_kdeplot = ff.create_distplot([filtered_data["price_per_sqr_meter"]], 
                                       group_labels=["price_per_sqr_meter"],
                                       curve_type="kde", 
                                       show_hist=False,
                                       show_rug=False,
                                       bin_size=.2)

    price_per_sqr_meter_kdeplot.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showticklabels=False, title=""),
        yaxis=dict(showticklabels=False, title=""),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )

    home_size_piechart = px.pie(filtered_data, values="price", names="home_size")
    
    home_size_piechart.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )

    grouped_df = filtered_data.groupby(['home_type', 'home_size']).price.mean().reset_index()
    pivot_df = grouped_df.pivot(index='home_type', 
                                columns='home_size', 
                                values='price')
    home_type_heatmap = px.imshow(pivot_df, text_auto=True, aspect="auto", color_continuous_scale='Viridis')
    home_type_heatmap.update_layout(
        # title='Average Home Price Heatmap', 
        xaxis=dict(title=""),
        yaxis=dict(title=""),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        # showlegend=False
    )

    return (
        f"{num_houses} listings",
        f"{avg_price:,.2f} €",
        f"{avg_area:,.2f} m2",
        f"{avg_price_per_sqr_meter:.2f} €/m2",
        bubble_chart, # scatter-plot
        price_kdeplot,
        area_kdeplot,
        price_per_sqr_meter_kdeplot,
        home_size_piechart,
        home_size_barchart, # home-size-distribution
        home_type_barchart, # home-type-distribution
        home_type_heatmap
    )


@app.callback(
    Output('popup', 'is_open'),
    Output('popup-content', 'children'),
    Input('scatter-plot', 'clickData'),
    State('popup', 'is_open')
)
def display_popup(clickData, is_open):

    if clickData:
        point = clickData['points'][0]
        municipality = point['customdata'][0]
        parish = point['customdata'][1]
        
        filtered_df = data[
            (data['municipality'] == municipality) &
            (data['parish'] == parish)
        ]
        
        avg_price_per_neighborhood = filtered_df.groupby('neighborhood')['price'].mean().reset_index()
        avg_area_per_neighborhood = filtered_df.groupby('neighborhood')['home_area'].mean().reset_index()
        avg_pricepmt_per_neighborhood = filtered_df.groupby('neighborhood')['price_per_sqr_meter'].mean().reset_index()

        price_chart = px.bar(
            avg_price_per_neighborhood,
            x='neighborhood',
            y='price',
            labels={'price': 'Average Price (€)', 
                    'neighborhood': 'Neighborhood'},
            title='Average Price per Neighborhood'
        )

        price_chart.update_layout(
            margin=dict(l=10, r=10, t=20, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            # showlegend=False
        )

        area_chart = px.bar(
            avg_area_per_neighborhood,
            x='neighborhood',
            y='home_area',
            labels={'home_area': 'Home Area (m2)', 
                    'neighborhood': 'Neighborhood'},
            title='Average Home Area per Neighborhood'
        )

        area_chart.update_layout(
            margin=dict(l=10, r=10, t=20, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            # showlegend=False
        )

        price_sqrmt_chart = px.bar(
            avg_pricepmt_per_neighborhood,
            x='neighborhood',
            y='price_per_sqr_meter',
            labels={'price_per_sqr_meter': 'Price per Sqr Meter (€/m2)', 
                    'neighborhood': 'Neighborhood'},
            title='Average Price per Sqr Meter per Neighborhood'
        )

        price_sqrmt_chart.update_layout(
            margin=dict(l=10, r=10, t=20, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            # showlegend=False
        )
        
        content = [
            dbc.Row([
                dbc.Col(dcc.Graph(figure=price_chart), width=4),
                dbc.Col(dcc.Graph(figure=area_chart), width=4),
                dbc.Col(dcc.Graph(figure=price_sqrmt_chart), width=4),
            ]),
            html.Div([
                html.P(f"Municipality: {municipality}"),
                html.P(f"Parish: {parish}"),
            ])
        ]

        return not is_open, content

    return is_open, ""
    

app.layout = layout

if __name__ == '__main__':
    server = app.server
