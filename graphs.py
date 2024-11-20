import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def calculate_payoff_data(spot_price, strike_price, option_price, option_type='call'):
    """Calculate payoff data."""
    # Generate price range from 50% to 150% of spot price
    prices = np.linspace(spot_price * 0.5, spot_price * 1.5, 100)
    
    if option_type == 'call':
        payoffs = np.maximum(prices - strike_price, 0) - option_price
    else:  # put
        payoffs = np.maximum(strike_price - prices, 0) - option_price
    
    return prices, payoffs



def create_option_payoff_charts(spot_price, strike_price, call_price, put_price):
    """Create interactive payoff diagrams for both call and put options."""

    # Create subplots
    fig = make_subplots(rows=1, cols=2, 
                    subplot_titles=('Call Option Payoff', 'Put Option Payoff'),
                    shared_yaxes=True)
    
    # Generate data for both options
    u_prices_for_call, call_payoffs = calculate_payoff_data(spot_price, strike_price, call_price, 'call')
    u_prices_for_put, put_payoffs = calculate_payoff_data(spot_price, strike_price, put_price, 'put')
    
    pos = call_payoffs >= 0
    neg = call_payoffs < 0 
    # Add call option trace
    fig.add_trace(
        go.Scatter(
            x=u_prices_for_call[pos],
            y=call_payoffs[pos],
            name='Call Payoff',
            line=dict(color='green'),
            fill='tonexty',
            # The fill color will be green above zero and red below
            fillcolor='rgba(0,255,0,0.2)',
            hovertemplate='Price: $%{x:.2f}<br>Profit/Loss: $%{y:.2f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Add another trace for the loss area (below zero)
    fig.add_trace(
        go.Scatter(
            x=u_prices_for_call[neg],
            y=call_payoffs[neg],
            name='Call Loss',
            line=dict(color='red'),
            fill='tonexty',
            fillcolor='rgba(255,0,0,0.2)',
            hovertemplate='Price: $%{x:.2f}<br>Profit/Loss: $%{y:.2f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    pos_p = put_payoffs >= 0
    neg_p = put_payoffs < 0 
    # Add put option trace (profit area)
    fig.add_trace(
        go.Scatter(
            x=u_prices_for_put[pos_p],
            y=put_payoffs[pos_p],
            name='Put Payoff',
            line=dict(color='green'),
            fill='tonexty',
            fillcolor='rgba(0,255,0,0.2)',
            hovertemplate='Price: $%{x:.2f}<br>Profit/Loss: $%{y:.2f}<extra></extra>'
        ),
        row=1, col=2
    )
    
    # Add put option loss area
    fig.add_trace(
        go.Scatter(
            x=u_prices_for_put[neg_p],
            y=put_payoffs[neg_p],
            name='Put Loss',
            line=dict(color='red'),
            fill='tonexty',
            fillcolor='rgba(255,0,0,0.2)',
            hovertemplate='Price: $%{x:.2f}<br>Profit/Loss: $%{y:.2f}<extra></extra>'
        ),
        row=1, col=2
    )
     # Add zero lines and current price lines to both plots
    for col in [1, 2]:
        # Zero line
        fig.add_hline(y=0, line=dict(color="black", dash="dash"), row=1, col=col)
        # Current price line
        fig.add_vline(x=spot_price, line=dict(color="blue", dash="dash"), row=1, col=col)
    
        # Update layout
        fig.update_layout(
            height=500,
            showlegend=False,
            title_text="",
            title_x=0.5,
            title_font_size=20,
            hoverlabel=dict(bgcolor="white"),
            # Make it responsive
            template="plotly_white"
        )
        
        # Update axes
        fig.update_xaxes(title_text="Price ($)", gridcolor='lightgrey')
        fig.update_yaxes(title_text="Profit/Loss ($)", gridcolor='lightgrey')
        
        return fig
