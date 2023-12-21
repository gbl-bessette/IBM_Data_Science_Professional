# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

print(max_payload)

# Preprocessing for Markdown Task 1
launch_sites_list = spacex_df['Launch Site'].unique().tolist()
options_md = [{'label': 'All Sites', 'value': 'ALL'}]
for site in launch_sites_list:
    options_md.append({'label': site, 'value': site})


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=options_md,
                                            value='ALL',
                                            placeholder="Select Launch Site",
                                            searchable=True
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)

def succes_pie_graph(dropdown_site):
    if dropdown_site == 'ALL':
        pie_df = spacex_df[['Launch Site', 'class']].groupby('Launch Site').sum().reset_index()
        pie_chart = px.pie(data_frame=pie_df, names='Launch Site', values='class', title='Total Success Launches by Site')
    else:
        pie_df = spacex_df[['class']][spacex_df['Launch Site']==dropdown_site].value_counts().reset_index()
        pie_chart = px.pie(data_frame=pie_df, names='class', values='count', title='Total Success Launches for Site ' + dropdown_site)
    return pie_chart

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')
)

def success_scatter_graph(dropdown_site, payload_limits):
    scatter_df = spacex_df[(spacex_df['Payload Mass (kg)'] <= payload_limits[1]) & (spacex_df['Payload Mass (kg)'] >= payload_limits[0])]

    if dropdown_site == 'ALL':
        scatter_chart = px.scatter(data_frame=scatter_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Success for all Sites')
    else:
        scatter_df = scatter_df[scatter_df['Launch Site']==dropdown_site]
        scatter_chart = px.scatter(data_frame=scatter_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Success for Site '+ dropdown_site)
    return scatter_chart

# Run the app
if __name__ == '__main__':
    app.run_server()
