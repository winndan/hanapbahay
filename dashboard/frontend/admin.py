from fasthtml.common import *  # Import FastHTML components
import fasthtml.common as fh
from monsterui.all import *  # Import MonsterUI for styled components
import numpy as np
import plotly.express as px
import pandas as pd

app, rt = fast_app(hdrs=Theme.slate.headers())

def generate_chart(num_points=30):
    df = pd.DataFrame({
        'Date': pd.date_range('2024-01-01', periods=num_points),
        'Revenue': np.random.normal(100, 10, num_points).cumsum(),
        'Users': np.random.normal(80, 8, num_points).cumsum(),
        'Growth': np.random.normal(60, 6, num_points).cumsum()
    })
    
    fig = px.line(df, x='Date', y=['Revenue', 'Users', 'Growth'], template='plotly_white', line_shape='spline')
    fig.update_traces(mode='lines+markers')
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10), hovermode='x unified',
        showlegend=True, legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
    )

    return fig.to_html(include_plotlyjs=True, full_html=False, config={'displayModeBar': False})

def InfoCard(title, value, change): 
    return Card(
        H3(value, cls="text-lg sm:text-xl md:text-2xl"),  # Responsive text
        P(change, cls="text-sm sm:text-md md:text-lg text-gray-500"),
        header=H4(title, cls="text-sm sm:text-md")
    )

info_card_data = [
    ("Total Revenue", "$45,231.89", "+20.1% from last month"),
    ("Subscriptions", "+2,350", "+180.1% from last month"),
    ("Sales", "+12,234", "+19% from last month"),
    ("Active Now", "+573", "+201 since last hour")
]

top_info_row = Grid(
    *[InfoCard(*row) for row in info_card_data],
    cls="info-grid"
)


def dashboard():
    return Title("Dashboard Example"), Container(
        Link(rel="stylesheet", href="/styles/admin.css"),
        Script(src="/styles/admin.js"),
        
        H2('Dashboard', cls="text-xl sm:text-2xl md:text-3xl font-bold"),
        
        # ✅ Tab Navigation (Now fully responsive)
        Nav(
            Ul(
                Li(A("Overview", href="#", data_tab="overview", cls="tab-button uk-active")),
                Li(A("Analytics", href="#", data_tab="analytics", cls="tab-button")),
                Li(A("Reports", href="#", data_tab="reports", cls="tab-button")),
                Li(A("Notifications", href="#", data_tab="notifications", cls="tab-button")),
                cls="uk-tab flex flex-wrap justify-center sm:justify-start gap-2"
            ),
            cls="flex justify-center sm:justify-start"
        ),

        # ✅ Tab Content (Initially hidden except overview)
        Div(
            Div(H3("Overview", cls="text-lg"), P("This is the overview section with key metrics."), top_info_row, id="overview", cls="tab-content"),
            Div(H3("Analytics", cls="text-lg"), P("Analytics dashboard with insights."), Card(Safe(generate_chart(50))), id="analytics", cls="tab-content"),
            Div(H3("Reports", cls="text-lg"), P("Reports section with detailed breakdowns."), id="reports", cls="tab-content"),
            Div(H3("Notifications", cls="text-lg"), P("User notifications and alerts."), id="notifications", cls="tab-content"),
            cls="space-y-4"
        ),
        cls="space-y-4 container mx-auto px-4 sm:px-8"
    )


