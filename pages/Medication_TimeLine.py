import dash
from dash_labs.plugins.pages import register_page
from dash import dcc, html, Input, Output, callback

from datetime import datetime as dt

from src.RandDataGen import rand_TimeLine
from src.Graphs import create_timeline,preprocess
import numpy as np
register_page(__name__)
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

server = app.server
app.config.suppress_callback_exceptions = True




df=rand_TimeLine()



admit_list=df["drug"].unique().tolist()
doctors=df.doctor.unique()
doctors= [i for i in df.doctor.unique() if i ]


def description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Medication Timeline"),
            html.H3("Welcome to Medication Timeline"),
            html.Div(
                id="intro",
                children="Here you can see information about your whole medication history, Explore your medication by date, doctors, or select specific drugs to show infromation about.",
            ),
        ],
    )


def generate_control_card():
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[


            html.P("Select doctor"),
            #html.Br(),
            dcc.Dropdown(
                id="doctor-select",
                options=[{"label": i, "value": i} for i in doctors],
                value=doctors[:],
                multi=True,
            ),
            html.Br(),
            html.P("Select Date Range"),
            dcc.DatePickerRange(
                id="date-picker-select",
                start_date=df.start_date[0].date(),
                end_date=df.end_date.iloc[-1].date(),
                min_date_allowed=df.start_date[0].date(),
                max_date_allowed=df.end_date.iloc[-1].date(),
                initial_visible_month=df.end_date.iloc[-1].date(),
            ),
            html.Br(),
            html.Br(),
            html.P("Select Drugs To Show"),
            dcc.Dropdown(
                id="drug-select",
                options=[{"label": i, "value": i} for i in admit_list],
                value=admit_list[:],
                multi=True,
            ),
            html.Br(),
            html.Div(
                id="reset-btn-outer",
                children=html.Button(id="reset-btn", children="Reset", n_clicks=0),
            ),
        ],
    )


_,intervals=preprocess(df)




layout = html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=app.get_asset_url("plotly_logo.png"))],style={"display":"none"}
        ),
        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[description_card(), generate_control_card()]
            + [
                html.Div(
                    ["initial child"], id="output-clientside", style={"display": "none"}
                )
            ],
        ),
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                # Patient Volume Heatmap
                html.Div(
                    id="patient_volume_card",
                    children=[
                        html.B("Medication Timeline"),
                        html.Hr(),
                        dcc.Graph(id="drug_timeline",style={"width":f"{sum([10+i[1]-i[0] for i in intervals])*(1+0.05*(len(intervals)-1))*12}px",
                            'height': f'{50*df.drug.nunique()}px',}) ,

                    ],style={"width":f"{sum([10+i[1]-i[0] for i in intervals])*(1+0.05*(len(intervals)-1))*12}px",
                            'height': f'{55*df.drug.nunique()}px',}
       
                    #style={'width':'1200', 'height':'800px'},
                ),
                # Patient Wait time by Department

            ], ),
    ],
)


@callback(
    Output("drug-select", "options"),
    Input("doctor-select", "value"),
    Input("date-picker-select", "start_date"),
    Input("date-picker-select", "end_date"),
    )
def update_drugs(doctors,start,end):
    return df[np.logical_and(df.start_date>=start,df.start_date<=end)][df.doctor.isin(doctors)]["drug"].unique().tolist()

@callback(
    Output("doctor-select", "options"),
    Input("date-picker-select", "start_date"),
    Input("date-picker-select", "end_date"),
    )
def update_drgswdocs(start,end):
    filterdf=df[np.logical_and(df.start_date>=start,df.start_date<=end)]
    doctors_filtrd= [i for i in filterdf.doctor.unique() if i ]
    return doctors_filtrd


@callback(
    Output("drug_timeline", "figure"),
    [
        Input("date-picker-select", "start_date"),
        Input("date-picker-select", "end_date"),
        Input("drug-select", "value"),
        Input("doctor-select", "value"),

        #Input("reset-btn", "n_clicks"),
    ],
)

def update_timeline(start,end,drugs,doctors):

    start = start + " 00:00:00"
    end = end + " 00:00:00"
    intervals=preprocess(df)

    # Return to original hm(no colored annotation) by resetting
    return create_timeline(
        df,start, end,drugs,doctors)


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
