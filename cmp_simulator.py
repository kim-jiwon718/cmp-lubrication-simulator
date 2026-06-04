import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title='CMP Lubrication Simulator', layout='wide')
st.title('CMP Slurry Flow Web Simulator')

U = st.sidebar.slider('Relative velocity U [m/s]', 0.1, 2.0, 0.5, 0.1)
eta_mPa = st.sidebar.slider('Slurry viscosity η [mPa·s]', 1.0, 20.0, 5.0, 0.5)
L_cm = st.sidebar.slider('Contact length L [cm]', 1.0, 10.0, 5.0, 0.5)
h1_um = st.sidebar.slider('Inlet gap height h1 [μm]', 50.0, 200.0, 100.0, 5.0)
h2_um = st.sidebar.slider('Outlet gap height h2 [μm]', 20.0, 150.0, 50.0, 5.0)

eta = eta_mPa * 1e-3
L = L_cm * 1e-2
h1 = h1_um * 1e-6
h2 = h2_um * 1e-6

if h1 <= h2:
    st.error('h1 must be larger than h2')
    st.stop()

x = np.linspace(0, L, 300)
h = h1 - (h1 - h2) * x / L

p = (6 * eta * U * L /(h1**2 - h2**2) * ((h1-h)*(h-h2)) / h**2)

fig = go.Figure()
fig.add_trace(go.Scatter(x=x*1000, y=p, mode='lines'))
fig.update_layout(title='Pressure Distribution',
                  xaxis_title='x [mm]',
                  yaxis_title='Pressure [Pa]')

st.plotly_chart(fig, use_container_width=True)
st.metric('Maximum Pressure', f'{np.max(p):.2f} Pa')

df = pd.DataFrame({'x_mm':x*1000,'pressure_Pa':p})
st.dataframe(df)
