import streamlit as st
import pandas as pd
import numpy as np
from graphs import create_option_payoff_charts
from BlackScholes import BlackScholes  

def create_app():
    st.set_page_config(
        page_title="Black-Scholes Option Calculator 📊",
        layout="wide",
        page_icon="📊",
    )

    # Title and description
    st.title("Black-Scholes Option Pricing Calculator")
    st.markdown("Calculate option prices and Greeks using the Black-Scholes model")

    # Sidebar for input parameters
    st.sidebar.title("Black-Scholes Model 📊")
    st.sidebar.write('*Created by*')
    linkedin_url = "https:/www.linkedin.com/in/silviopetruzzi"
    st.sidebar.markdown(
        f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;">'
        f'<img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" '
        f'style="vertical-align: middle; margin-right: 10px;">Silvio Petruzzi</a>',
        unsafe_allow_html=True,
    )
    st.sidebar.subheader("Tweak input parameters")
    st.sidebar.markdown("Adjust the parameters below:")

    # Input parameters in the sidebar
    S = st.sidebar.number_input(
        "Spot Price",
        min_value=0.01,
        value=100.00,
        step=0.50,
        format="%.2f"
    )

    K = st.sidebar.number_input(
        "Strike Price",
        min_value=0.01,
        value=100.00,
        step=0.50,
        format="%.2f"
    )

    t = st.sidebar.number_input(
        "Time to Maturity (Years)",
        min_value=0.01,
        value=1.00,
        step=0.01,
        format="%.2f"
    )

    sigma = st.sidebar.number_input(
        "Volatility (σ)",
        min_value=0.01,
        value=0.20,
        step=0.01,
        format="%.2f"
    )

    r = st.sidebar.number_input(
        "Risk-Free Rate",
        min_value=0.00,
        value=0.030,
        step=0.001,
        format="%.3f"
    )

    params = {
        "Current Price": [S],
        "Strike Price": [K],
        "Time-to-maturity": [t],
        "vol": [sigma],
        "risk-free-rate": [r]
    }
 
    # calculate prices
    # Create instance of BlackScholes class
    bs_call = BlackScholes(S, K, t, r, sigma)
    bs_put = BlackScholes(S, K, t, r, sigma, option_type='put')
        
        # Calculate option prices
    call_price = bs_call.calculate_price()
    
    put_price = bs_put.calculate_price()
    # Calculate Greeks
    delta_call = bs_call.get_delta()
    delta_put = bs_put.get_delta()
    gamma_call = bs_call.get_gamma()
    gamma_put = bs_put.get_gamma()
    theta_call = bs_call.get_theta()
    theta_put = bs_put.get_theta()
    vega_call = bs_call.get_vega()
    vega_put = bs_put.get_vega()
    rho_call = bs_call.get_rho()
    rho_put = bs_put.get_rho()

    # Display results in two columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Call Option")
        st.write(f'**Price**: ${call_price:.2f}')

        call_metrics = {
            "Delta": [delta_call],
            "Gamma": [gamma_call],
            "Theta": [theta_call],
            "Vega" : [vega_call],
            "Rho": [rho_call],
        }

        st.dataframe(call_metrics)

    with col2:
        st.subheader("Put Option")
        st.write(f'**Price**: ${put_price:.2f}')
        put_metrics = {
            "Delta": [delta_put],
            "Gamma": [gamma_put],
            "Theta": [theta_put],
            "Vega" : [vega_put],
            "Rho": [rho_put]
        }

        st.dataframe(put_metrics)

    def calculate_payoff_data(spot_price, strike_price, option_price, option_type='call'):
        """Calculate payoff data."""
        # Generate price range from 50% to 150% of spot price
        prices = np.linspace(spot_price * 0.5, spot_price * 1.5, 100)
        
        if option_type == 'call':
            payoffs = np.maximum(prices - strike_price, 0) - option_price
        else:  # put
            payoffs = np.maximum(strike_price - prices, 0) - option_price
        
        return prices, payoffs
    
    st.subheader('**P&L Graphs**')

    # Create and display the payoff diagrams
    fig = create_option_payoff_charts(S, K, call_price, put_price)
    st.plotly_chart(fig, use_container_width=True)

    # Add styling to center-align
    st.markdown(
        """
        <style>
        .centered-table {
            display: flex;
            justify-content: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Wrap the table in a div with the centered-table class
    st.markdown('<div class="centered-table">', unsafe_allow_html=True)
    st.table(params)
    st.markdown('</div>', unsafe_allow_html=True)
    


if __name__ == "__main__":
    create_app()
