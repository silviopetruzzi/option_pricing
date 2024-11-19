import streamlit as st
import pandas as pd
from BlackScholes import BlackScholes  

def create_app():
    # Set page config
    st.set_page_config(
        page_title="Black-Scholes Option Calculator 📊",
        layout="wide",
        page_icon="📊",
    )

    # Title and description
    st.title("Black-Scholes Option Calculator")
    st.write('Created by: ')
    linkedin_url ="https:/www.linkedin.com/in/silviopetruzzi"
    st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Silvio Petruzzi`</a>', unsafe_allow_html=True)
    st.markdown("Calculate option prices and Greeks using the Black-Scholes model")

    # Create two columns for input parameters
    col1, col2 = st.columns(2)

    with col1:
        # Input parameters
        S = st.number_input(
            "Spot Price",
            min_value=0.01,
            value=100.00,
            step=0.01,
            format="%.2f"
        )
        
        K = st.number_input(
            "Strike Price",
            min_value=0.01,
            value=100.00,
            step=0.01,
            format="%.2f"
        )
        
        t = st.number_input(
            "Time to Maturity (Years)",
            min_value=0.01,
            value=1.00,
            step=0.01,
            format="%.2f"
        )

    with col2:
        sigma = st.number_input(
            "Volatility (σ)",
            min_value=0.01,
            value=0.20,
            step=0.01,
            format="%.2f"
        )
        
        r = st.number_input(
            "Risk-Free Rate",
            min_value=0.00,
            value=0.030,
            step=0.001,
            format="%.3f"
        ) 
 
    # Calculate button
    if st.button("Calculate", type="primary"):
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
            call_metrics = {
                "**Price**": f"${call_price:.2f}",
                "Delta": f"{delta_call:.4f}",
                "Gamma": f"{gamma_call:.4f}",
                "Theta": f"{theta_call:.4f}",
                "Vega" : f"{vega_call:.4f}",
                "Rho": f"{rho_call:.4f}"
            }
            st.markdown("\n\n".join(f"{k}: {v}" for k, v in call_metrics.items()))

        with col2:
            st.subheader("Put Option")
            put_metrics = {
                "**Price**": f"${put_price:.2f}",
                "Delta": f"{delta_put:.4f}",
                "Gamma": f"{gamma_put:.4f}",
                "Theta": f"{theta_put:.4f}",
                "Vega" : f"{vega_put:.4f}",
                "Rho": f"{rho_put:.4f}"
            }
            st.markdown("\n\n".join(f"{k}: {v}" for k, v in put_metrics.items()))

if __name__ == "__main__":
    create_app()
