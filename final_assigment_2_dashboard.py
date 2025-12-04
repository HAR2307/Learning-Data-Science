
import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
#app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([

    # TASK 2.1 Title
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': '24px'}
    ),

    # TASK 2.2 Dropdowns
    html.Div([

        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Yearly Statistics',    
            placeholder='Select a report type'
        ),

        html.Br(),

        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select year',
            value=1980
        ),

        html.Br(),

        # TASK 2.3 Output area
        html.Div(
            id='output-container',
            className='division',
            style={'display': 'flex'}
        )

    ])   
])  


#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics': 
        return False
    else: 
        return True

#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output('output-container', 'children'),
    [
        Input('dropdown-statistics', 'value'),
        Input('select-year', 'value')
    ]
)


def update_output_container(selected_statistics,input_year):
    if selected_statistics == 'Recession':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        
#TASK 2.5: Create and display graphs for Recession Report Statistics

#Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        # use groupby to create relevant data for plotting
        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"))

#Plot 2 Calculate the average number of vehicles sold by vehicle type       
        
        # use groupby to create relevant data for plotting
        #Hint:Use Vehicle_Type and Automobile_Sales columns
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()                 
        R_chart2  = dcc.Graph(
            figure=px.bar(average_sales,
            x='Vehicle_Type',
            y='Automobile_Sales',
            title="Average Automobile Sales by vehicle type"))
        
# Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        # grouping data for plotting
	# Hint:Use Vehicle_Type and Advertising_Expenditure columns
        exp_rec=  recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()

        R_chart3 = dcc.Graph(figure = px.pie(values=exp_rec['Advertising_Expenditure'], 
                                             names=exp_rec['Vehicle_Type'], 
                                             title='Total advertising expenditure share by vehicle type')
)

# Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        #grouping data for plotting
	# Hint:Use unemployment_rate,Vehicle_Type and Automobile_Sales columns
        unemp_data = recession_data.groupby(['unemployment_rate','Vehicle_Type'])['Automobile_Sales'].mean().reset_index()

        R_chart4 = dcc.Graph(figure=px.bar(unemp_data, x='Vehicle_Type', 
                                           y='unemployment_rate', 
                                           labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'}, 
                                           color = 'unemployment_rate',
                                           title='Effect of Unemployment Rate on Vehicle Type and Sales'))


        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1),html.Div(children=R_chart1)],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart2),html.Div(children=R_chart2)],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3),html.Div(children=R_chart3)],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart4),html.Div(children=R_chart4)],style={'display': 'flex'})
            ]

# TASK 2.6: Create and display graphs for Yearly Report Statistics
 # Yearly Statistic Report Plots
    # Check for Yearly Statistics.                             
    elif (input_year and selected_statistics=='Yearly Statistics') :
        yearly_data = data[data['Year'] == input_year]
                              

                              
#plot 1 Yearly Automobile sales using line chart for the whole period.
        # grouping data for plotting.
        # Hint:Use the columns Year and Automobile_Sales.
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()

        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title='Average Automobile Sales by Year'
            ).update_xaxes(
                dtick=1,             # show every year
                tickangle=45,        # rotate labels
                tickfont=dict(size=10),  # make x-axis tick labels smaller
                title='Year'
            ).update_yaxes(
                tickfont=dict(size=10),  # make y-axis tick labels smaller
                title='Average Automobile Sales'
            )
        )
            
# Plot 2 Total Monthly Automobile sales using line chart.
        # grouping data for plotting.
	# Hint:Use the columns Month and Automobile_Sales.
        mas=data[data['Year'] == input_year].groupby('Month')['Automobile_Sales'].sum().reset_index()

        Y_chart2 = dcc.Graph(figure=px.line(mas,
            x='Month',
            y='Automobile_Sales',
            title='Total Monthly Automobile Sales in the year {}'.format(input_year)))

  # Plot bar chart for average number of vehicles sold during the given year
         # grouping data for plotting.
         # Hint:Use the columns Year and Automobile_Sales
        avr_vdata=yearly_data.groupby(['Vehicle_Type','Year'])['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph( figure =px.bar(avr_vdata,
                                             x = 'Vehicle_Type' ,
                                             y = 'Automobile_Sales',
                                             color = 'Vehicle_Type',
                                             title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))

    # Total Advertisement Expenditure for each vehicle using pie chart
         # grouping data for plotting.
         # Hint:Use the columns Vehicle_Type and Advertising_Expenditure
        exp_data=yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure = px.pie(values=exp_data['Advertising_Expenditure'], 
                                             names=exp_data['Vehicle_Type'], 
                                             title='Total Advertisement Expenditure for each vehicle type in the year {}'.format(input_year)))

#TASK 2.6: Returning the graphs for displaying Yearly data
        return [
                html.Div(className='chart-item', children=[html.Div(children=Y_chart1),html.Div(children=Y_chart1)],style={'display': 'flex'}),
                html.Div(className='chart-item', children=[html.Div(children=Y_chart2),html.Div(children=Y_chart2)],style={'display': 'flex'}),
                html.Div(className='chart-item', children=[html.Div(children=Y_chart3),html.Div(children=Y_chart3)],style={'display': 'flex'}),
                html.Div(className='chart-item', children=[html.Div(children=Y_chart4),html.Div(children=Y_chart4)],style={'display': 'flex'})
                ]
    
    
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run()

