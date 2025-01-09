# Import necessary libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Sales Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years
year_list = [i for i in range(1980, 2024)]

#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    # Title for the dashboard
    html.H1('Automobile Sales Statistics Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
    
    # Dropdown for selecting the report type
    html.Div([
        html.Label("Select Report Type:", style={'font-size': 20, 'text-align': 'center'}),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            placeholder='Select a report type',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'textAlign': 'center'}
        )
    ], style={'margin': '20px'}),

    # Dropdown for selecting the year
    html.Div([
        html.Label("Select Year:", style={'font-size': 20, 'text-align': 'center'}),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select Year',
            value=2023,
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'textAlign': 'center'}
        )
    ], style={'margin': '20px'}),

    # Division for output display
    html.Div(id='output-container', style={'margin-top': '20px'})
])

#---------------------------------------------------------------------------------------
# Disable the year dropdown unless "Yearly Statistics" is selected
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_year_dropdown(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False  # Enable for yearly statistics
    else:
        return True  # Disable for recession period statistics

# Callback for generating the output container based on selected report type
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), 
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        
        # Plot 1: Average automobile sales over recession periods
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Average Automobile Sales During Recession"))

        # Plot 2: Average sales by vehicle type during recession
        avg_sales_by_type = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(figure=px.bar(avg_sales_by_type, x='Vehicle_Type', y='Automobile_Sales', title="Average Sales by Vehicle Type During Recession"))

        # Pie chart for advertising expenditure during recession
        exp_by_type = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(exp_by_type, names='Vehicle_Type', values='Advertising_Expenditure', title="Advertising Expenditure Share by Vehicle Type"))

        # Plot for unemployment rate and vehicle sales
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type', title="Effect of Unemployment Rate on Sales"))

        return [
            html.Div(children=[R_chart1, R_chart2], style={'display': 'flex'}),
            html.Div(children=[R_chart3, R_chart4], style={'display': 'flex'})
        ]

    elif selected_statistics == 'Yearly Statistics' and input_year:
        yearly_data = data[data['Year'] == input_year]

        # Plot 1: Yearly automobile sales
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales', title='Yearly Automobile Sales'))

        # Plot 2: Monthly automobile sales for selected year
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(mas, x='Month', y='Automobile_Sales', title=f'Total Monthly Sales in {input_year}'))

        # Bar chart for average sales by vehicle type in selected year
        avg_vtype_data = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avg_vtype_data, x='Vehicle_Type', y='Automobile_Sales', title=f'Average Vehicles Sold by Type in {input_year}'))

        # Pie chart for advertisement expenditure in selected year
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data, names='Vehicle_Type', values='Advertising_Expenditure', title='Advertisement Expenditure by Vehicle Type'))

        return [
            html.Div(children=[Y_chart1, Y_chart2], style={'display': 'flex'}),
            html.Div(children=[Y_chart3, Y_chart4], style={'display': 'flex'})
        ]
    else:
        return html.Div("Please select valid report type and year.", style={'color': 'red', 'textAlign': 'center'})

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
