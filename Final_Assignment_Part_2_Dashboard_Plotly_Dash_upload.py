"""
Final Assignment: Part 2 - Create Dashboard with Plotly and Dash
Analyzing the Impact of Recession on Automobile Sales

This is a self-contained Dash application. It includes:
- Year / recession selectors
- KPI cards
- Yearly automobile-sales line chart
- Average sales by vehicle type bar chart
- Advertising expenditure pie chart
- Recession sales trend chart
- Price vs sales scatter plot
- Interactive callbacks

Run:
    python Final_Assignment_Part_2_Dashboard_Plotly_Dash.py

Then open the local address shown in the terminal.
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# ---------------------------------------------------------------------
# 1. DATA PREPARATION
# ---------------------------------------------------------------------

np.random.seed(42)

recession_years = {1980, 1981, 1982, 1991, 2000, 2001, 2008, 2009, 2020}

vehicle_types = [
    "Supperminicar",
    "Smallfamiliycar",
    "Mediumfamilycar",
    "Executivecar",
    "Sports"
]

cities = ["California", "New York", "Illinois", "Georgia"]

rows = []

for year in range(1980, 2021):
    months = range(1, 13)

    # The 2020 recession is represented by the final four months.
    if year == 2020:
        months = range(9, 13)

    for month in months:
        recession = int(year in recession_years)

        seasonality = {
            1: 0.50, 2: 0.75, 3: 1.50, 4: 1.00,
            5: 1.50, 6: 0.75, 7: 0.50, 8: 0.25,
            9: 0.07, 10: 0.12, 11: 0.07, 12: 0.25
        }[month]

        base_sales = 3600 if not recession else 900
        trend = (year - 1980) * 22
        seasonal_effect = (seasonality - 0.5) * 750
        noise = np.random.normal(0, 260)

        sales = max(
            250,
            base_sales + trend + seasonal_effect + noise
        )

        gdp = max(
            10,
            25 + (year - 1980) * 0.85
            + np.random.normal(0, 8)
            - recession * 7
        )

        unemployment = max(
            1.2,
            2.2 + np.random.normal(0, 0.65)
            + recession * 1.8
        )

        confidence = max(
            70,
            112 + np.random.normal(0, 8)
            - recession * 12
        )

        price = max(
            12000,
            22000 + (year - 1980) * 350
            + np.random.normal(0, 2500)
        )

        advertising = max(
            800,
            np.random.normal(3300, 850)
        )

        competition = np.random.randint(3, 10)
        vehicle = np.random.choice(
            vehicle_types,
            p=[0.25, 0.25, 0.30, 0.12, 0.08]
        )
        city = np.random.choice(cities)

        rows.append([
            pd.Timestamp(year=year, month=month, day=1)
            + pd.offsets.MonthEnd(0),
            year,
            pd.Timestamp(year=year, month=month, day=1).strftime("%b"),
            recession,
            confidence,
            seasonality,
            price,
            advertising,
            competition,
            gdp,
            np.random.normal(0, 0.5),
            unemployment,
            sales,
            vehicle,
            city
        ])

columns = [
    "Date",
    "Year",
    "Month",
    "Recession",
    "Consumer_Confidence",
    "Seasonality_Weight",
    "Price",
    "Advertising_Expenditure",
    "Competition",
    "GDP",
    "Growth_Rate",
    "unemployment_rate",
    "Automobile_Sales",
    "Vehicle_Type",
    "City"
]

df = pd.DataFrame(rows, columns=columns)

# ---------------------------------------------------------------------
# 2. DASH APPLICATION
# ---------------------------------------------------------------------

app = Dash(__name__)
app.title = "Automobile Sales Dashboard"

years = sorted(df["Year"].unique())

app.layout = html.Div(
    style={
        "fontFamily": "Arial",
        "backgroundColor": "#f5f7fa",
        "padding": "20px"
    },
    children=[

        html.H1(
            "Automobile Sales Statistics Dashboard",
            style={
                "textAlign": "center",
                "color": "#1f2937",
                "marginBottom": "5px"
            }
        ),

        html.P(
            "Final Assignment – Part 2: Create Dashboard with Plotly and Dash",
            style={
                "textAlign": "center",
                "color": "#64748b",
                "fontSize": "16px"
            }
        ),

        # -------------------------------------------------------------
        # FILTERS
        # -------------------------------------------------------------
        html.Div(
            style={
                "display": "flex",
                "gap": "20px",
                "justifyContent": "center",
                "margin": "20px 0"
            },
            children=[

                html.Div(
                    style={"width": "300px"},
                    children=[
                        html.Label(
                            "Select Year",
                            style={"fontWeight": "bold"}
                        ),
                        dcc.Dropdown(
                            id="year-dropdown",
                            options=[
                                {"label": "All Years", "value": "ALL"}
                            ] + [
                                {"label": str(y), "value": int(y)}
                                for y in years
                            ],
                            value="ALL",
                            clearable=False
                        )
                    ]
                ),

                html.Div(
                    style={"width": "300px"},
                    children=[
                        html.Label(
                            "Select Economic Period",
                            style={"fontWeight": "bold"}
                        ),
                        dcc.Dropdown(
                            id="period-dropdown",
                            options=[
                                {"label": "All Periods", "value": "ALL"},
                                {"label": "Recession", "value": 1},
                                {"label": "Non-Recession", "value": 0}
                            ],
                            value="ALL",
                            clearable=False
                        )
                    ]
                )
            ]
        ),

        # -------------------------------------------------------------
        # KPI CARDS
        # -------------------------------------------------------------
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns":
                    "repeat(4, 1fr)",
                "gap": "15px",
                "marginBottom": "20px"
            },
            children=[
                html.Div(
                    [
                        html.H4("Total Automobile Sales"),
                        html.H2(id="sales-kpi")
                    ],
                    style={
                        "backgroundColor": "white",
                        "padding": "18px",
                        "borderRadius": "10px",
                        "textAlign": "center",
                        "boxShadow": "0 2px 8px rgba(0,0,0,0.08)"
                    }
                ),

                html.Div(
                    [
                        html.H4("Average Vehicle Price"),
                        html.H2(id="price-kpi")
                    ],
                    style={
                        "backgroundColor": "white",
                        "padding": "18px",
                        "borderRadius": "10px",
                        "textAlign": "center",
                        "boxShadow": "0 2px 8px rgba(0,0,0,0.08)"
                    }
                ),

                html.Div(
                    [
                        html.H4("Average GDP"),
                        html.H2(id="gdp-kpi")
                    ],
                    style={
                        "backgroundColor": "white",
                        "padding": "18px",
                        "borderRadius": "10px",
                        "textAlign": "center",
                        "boxShadow": "0 2px 8px rgba(0,0,0,0.08)"
                    }
                ),

                html.Div(
                    [
                        html.H4("Average Unemployment"),
                        html.H2(id="unemployment-kpi")
                    ],
                    style={
                        "backgroundColor": "white",
                        "padding": "18px",
                        "borderRadius": "10px",
                        "textAlign": "center",
                        "boxShadow": "0 2px 8px rgba(0,0,0,0.08)"
                    }
                )
            ]
        ),

        # -------------------------------------------------------------
        # GRAPHS
        # -------------------------------------------------------------
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gap": "20px"
            },
            children=[

                html.Div(
                    dcc.Graph(id="yearly-sales-chart"),
                    style={
                        "backgroundColor": "white",
                        "padding": "10px",
                        "borderRadius": "10px"
                    }
                ),

                html.Div(
                    dcc.Graph(id="vehicle-sales-chart"),
                    style={
                        "backgroundColor": "white",
                        "padding": "10px",
                        "borderRadius": "10px"
                    }
                ),

                html.Div(
                    dcc.Graph(id="advertising-chart"),
                    style={
                        "backgroundColor": "white",
                        "padding": "10px",
                        "borderRadius": "10px"
                    }
                ),

                html.Div(
                    dcc.Graph(id="recession-chart"),
                    style={
                        "backgroundColor": "white",
                        "padding": "10px",
                        "borderRadius": "10px"
                    }
                ),

                html.Div(
                    dcc.Graph(id="price-sales-chart"),
                    style={
                        "backgroundColor": "white",
                        "padding": "10px",
                        "borderRadius": "10px",
                        "gridColumn": "1 / -1"
                    }
                )
            ]
        ),

        html.Hr(),

        html.P(
            "Dashboard created using Python, Pandas, Plotly and Dash.",
            style={
                "textAlign": "center",
                "color": "#64748b"
            }
        )
    ]
)

# ---------------------------------------------------------------------
# 3. CALLBACK
# ---------------------------------------------------------------------

@app.callback(
    Output("sales-kpi", "children"),
    Output("price-kpi", "children"),
    Output("gdp-kpi", "children"),
    Output("unemployment-kpi", "children"),
    Output("yearly-sales-chart", "figure"),
    Output("vehicle-sales-chart", "figure"),
    Output("advertising-chart", "figure"),
    Output("recession-chart", "figure"),
    Output("price-sales-chart", "figure"),
    Input("year-dropdown", "value"),
    Input("period-dropdown", "value")
)
def update_dashboard(selected_year, selected_period):

    filtered = df.copy()

    if selected_year != "ALL":
        filtered = filtered[
            filtered["Year"] == int(selected_year)
        ]

    if selected_period != "ALL":
        filtered = filtered[
            filtered["Recession"] == int(selected_period)
        ]

    # -------------------------------------------------------------
    # KPI calculations
    # -------------------------------------------------------------
    total_sales = filtered["Automobile_Sales"].sum()
    avg_price = filtered["Price"].mean()
    avg_gdp = filtered["GDP"].mean()
    avg_unemployment = filtered["unemployment_rate"].mean()

    # -------------------------------------------------------------
    # Task: Yearly automobile sales
    # -------------------------------------------------------------
    yearly = (
        filtered.groupby("Year", as_index=False)
        ["Automobile_Sales"].sum()
    )

    fig_yearly = px.line(
        yearly,
        x="Year",
        y="Automobile_Sales",
        markers=True,
        title="Yearly Automobile Sales"
    )

    fig_yearly.update_layout(
        xaxis_title="Year",
        yaxis_title="Automobile Sales",
        template="plotly_white"
    )

    # -------------------------------------------------------------
    # Task: Average sales by vehicle type
    # -------------------------------------------------------------
    vehicle = (
        filtered.groupby("Vehicle_Type", as_index=False)
        ["Automobile_Sales"].mean()
    )

    fig_vehicle = px.bar(
        vehicle,
        x="Vehicle_Type",
        y="Automobile_Sales",
        title="Average Automobile Sales by Vehicle Type"
    )

    fig_vehicle.update_layout(
        xaxis_title="Vehicle Type",
        yaxis_title="Average Sales",
        template="plotly_white"
    )

    # -------------------------------------------------------------
    # Task: Advertising expenditure
    # -------------------------------------------------------------
    advertising = (
        filtered.groupby("Vehicle_Type", as_index=False)
        ["Advertising_Expenditure"].sum()
    )

    fig_advertising = px.pie(
        advertising,
        names="Vehicle_Type",
        values="Advertising_Expenditure",
        title="Advertising Expenditure by Vehicle Type"
    )

    # -------------------------------------------------------------
    # Task: Recession/non-recession comparison
    # -------------------------------------------------------------
    period = (
        filtered.groupby("Recession", as_index=False)
        ["Automobile_Sales"].mean()
    )

    period["Period"] = period["Recession"].map(
        {0: "Non-Recession", 1: "Recession"}
    )

    fig_recession = px.bar(
        period,
        x="Period",
        y="Automobile_Sales",
        title="Average Sales: Recession vs Non-Recession",
        text_auto=".2s"
    )

    fig_recession.update_layout(
        xaxis_title="Economic Period",
        yaxis_title="Average Automobile Sales",
        template="plotly_white"
    )

    # -------------------------------------------------------------
    # Task: Price vs sales
    # -------------------------------------------------------------
    fig_price = px.scatter(
        filtered,
        x="Price",
        y="Automobile_Sales",
        color="Vehicle_Type",
        size="Advertising_Expenditure",
        hover_data=[
            "Year",
            "Recession",
            "GDP",
            "unemployment_rate"
        ],
        title="Vehicle Price vs Automobile Sales"
    )

    fig_price.update_layout(
        xaxis_title="Vehicle Price",
        yaxis_title="Automobile Sales",
        template="plotly_white"
    )

    return (
        f"{total_sales:,.0f}",
        f"${avg_price:,.0f}",
        f"{avg_gdp:,.2f}",
        f"{avg_unemployment:.2f}%",
        fig_yearly,
        fig_vehicle,
        fig_advertising,
        fig_recession,
        fig_price
    )


# ---------------------------------------------------------------------
# 4. RUN APPLICATION
# ---------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
