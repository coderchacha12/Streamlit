import streamlit as st

def main():

    import streamlit as st

    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import numpy as np

    st.title("UPI Banks KPI Dashboard")
    # Custom CSS
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #1f4e79;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: bold;
        }
        .kpi-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 1rem;
            color: white;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .kpi-value {
            font-size: 2rem;
            font-weight: bold;
            margin: 0.5rem 0;
        }
        .kpi-label {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        .performance-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.8rem;
            font-weight: bold;
        }
        .excellent { background-color: #10b981; color: white; }
        .good { background-color: #3b82f6; color: white; }
        .average { background-color: #f59e0b; color: white; }
        .poor { background-color: #ef4444; color: white; }
    </style>
    """, unsafe_allow_html=True)

    # Load data from CSV
    @st.cache_data
    def load_data():
        try:
            df = pd.read_csv(r'C:\Users\Shailendra\Desktop\upi streamlit\banks.csv')
            
            # Clean percentage columns
            percentage_cols = ['Approved %', 'TD%', 'Debit Reversal Success %']
            for col in percentage_cols:
                df[col] = df[col].str.replace('%', '').astype(float)
            
            return df
        except FileNotFoundError:
            # Sample data for demo with multiple months
            banks = [
                'State Bank Of India', 'HDFC Bank Ltd', 'Bank of Baroda',
                'Union Bank of India', 'ICICI Bank', 'Paytm Payments Bank',
                'Axis Bank Ltd', 'Punjab National Bank', 'Canara Bank',
                'Kotak Mahindra Bank', 'Bank of India', 'Indian Bank',
                'Central Bank Of India', 'IDBI Bank Limited', 'Federal Bank',
                'Airtel Payments Bank'
            ]
            
            base_volumes = [1291.88, 406.61, 299.12, 287.21, 274.0, 262.28,
                        243.68, 213.48, 206.3, 186.34, 171.56, 115.76,
                        95.53, 66.58, 62.84, 62.35]
            
            base_approval = [91.70, 94.01, 92.13, 90.21, 95.14, 94.95, 95.25, 92.49,
                            92.47, 94.30, 93.02, 88.38, 90.13, 94.57, 93.07, 86.08]
            
            base_td = [1.21, 0.29, 0.49, 0.97, 0.17, 0.08, 0.25, 0.61, 0.47, 0.29,
                    1.60, 5.33, 2.90, 0.75, 1.55, 1.98]
            
            base_reversal = [95.66, 91.30, 98.88, 46.80, 69.88, 94.04, 97.79, 90.03,
                            92.99, 86.27, 50.40, 40.42, 63.32, 64.13, 71.18, 72.95]
            
            # Generate data for multiple months
            months = ['Apr 2022', 'May 2022', 'Jun 2022', 'Jul 2022', 'Aug 2022', 'Sep 2022']
            all_data = []
            
            for month_idx, month in enumerate(months):
                for bank_idx, bank in enumerate(banks):
                    # Add some variation to simulate real monthly changes
                    growth_factor = 1 + (month_idx * 0.05) + np.random.uniform(-0.1, 0.15)
                    approval_variation = np.random.uniform(-2, 3)
                    td_variation = np.random.uniform(-0.5, 1.0)
                    reversal_variation = np.random.uniform(-5, 8)
                    
                    volume = max(base_volumes[bank_idx] * growth_factor, 0)
                    approval = max(min(base_approval[bank_idx] + approval_variation, 100), 70)
                    td = max(base_td[bank_idx] + td_variation, 0.01)
                    reversal = max(min(base_reversal[bank_idx] + reversal_variation, 100), 30)
                    
                    all_data.append([month, bank, volume, approval, td, reversal])
            
            df = pd.DataFrame(all_data, columns=['Month', 'UPI Remitter Banks', 'Total Volume (In Mn)', 
                                            'Approved %', 'TD%', 'Debit Reversal Success %'])
            return df

    # Load data
    df = load_data()

    # Helper function to get performance badge
    def get_performance_badge(value, metric_type):
        if metric_type == 'approval':
            if value >= 95: return "excellent", "Excellent"
            elif value >= 92: return "good", "Good"
            elif value >= 88: return "average", "Average"
            else: return "poor", "Poor"
        elif metric_type == 'td':
            if value <= 0.5: return "excellent", "Excellent"
            elif value <= 1.0: return "good", "Good"
            elif value <= 2.0: return "average", "Average"
            else: return "poor", "Poor"
        elif metric_type == 'reversal':
            if value >= 90: return "excellent", "Excellent"
            elif value >= 80: return "good", "Good"
            elif value >= 70: return "average", "Average"
            else: return "poor", "Poor"

    # Main header
    st.markdown('<h1 class="main-header">🏛️ UPI Banks Performance KPI Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Banking Performance Analytics & Success Metrics</p>', unsafe_allow_html=True)

    # Sidebar filters
    st.sidebar.header("📊 Dashboard Controls")
    available_months = sorted(df['Month'].unique())
    selected_month = st.sidebar.selectbox("Select Month:", available_months, index=len(available_months)-1)

    # Show month-over-month comparison option
    if len(available_months) > 1:
        show_comparison = st.sidebar.checkbox("Show Month-over-Month Comparison", value=False)
        if show_comparison and len(available_months) > 1:
            previous_month_idx = max(0, available_months.index(selected_month) - 1)
            comparison_month = available_months[previous_month_idx]
        else:
            comparison_month = None
    else:
        show_comparison = False
        comparison_month = None

    # Filter data
    filtered_df = df[df['Month'] == selected_month].copy()

    # Get comparison data if enabled
    if show_comparison and comparison_month:
        comparison_df = df[df['Month'] == comparison_month].copy()
        
        # Calculate month-over-month changes
        merged_df = filtered_df.merge(comparison_df, on='UPI Remitter Banks', suffixes=('_current', '_previous'))
        merged_df['Volume_Change'] = ((merged_df['Total Volume (In Mn)_current'] - merged_df['Total Volume (In Mn)_previous']) / merged_df['Total Volume (In Mn)_previous'] * 100)
        merged_df['Approval_Change'] = merged_df['Approved %_current'] - merged_df['Approved %_previous']
    else:
        comparison_df = None
        merged_df = None

    # Calculate KPIs
    total_volume = filtered_df['Total Volume (In Mn)'].sum()
    avg_approval_rate = filtered_df['Approved %'].mean()
    avg_td_rate = filtered_df['TD%'].mean()
    avg_reversal_rate = filtered_df['Debit Reversal Success %'].mean()
    top_performer = filtered_df.loc[filtered_df['Total Volume (In Mn)'].idxmax(), 'UPI Remitter Banks']
    market_leader_volume = filtered_df['Total Volume (In Mn)'].max()
    market_share_leader = (market_leader_volume / total_volume) * 100

    # KPI Cards Section
    st.markdown("## 🎯 Key Performance Indicators")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        volume_delta = ""
        if show_comparison and comparison_df is not None:
            prev_volume = comparison_df['Total Volume (In Mn)'].sum()
            volume_change = ((total_volume - prev_volume) / prev_volume * 100)
            volume_delta = f"vs {comparison_month}"
        
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Transaction Volume</div>
            <div class="kpi-value">{total_volume:,.0f}M</div>
            <div class="kpi-label">{len(filtered_df)} Active Banks {volume_delta}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        approval_class, approval_label = get_performance_badge(avg_approval_rate, 'approval')
        approval_delta = ""
        if show_comparison and comparison_df is not None:
            prev_approval = comparison_df['Approved %'].mean()
            approval_change = avg_approval_rate - prev_approval
            approval_delta = f"({approval_change:+.1f}% vs prev)"
        
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Average Approval Rate</div>
            <div class="kpi-value">{avg_approval_rate:.1f}%</div>
            <span class="performance-badge {approval_class}">{approval_label}</span>
            <div class="kpi-label">{approval_delta}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        td_class, td_label = get_performance_badge(avg_td_rate, 'td')
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Average Technical Decline</div>
            <div class="kpi-value">{avg_td_rate:.2f}%</div>
            <span class="performance-badge {td_class}">{td_label}</span>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        reversal_class, reversal_label = get_performance_badge(avg_reversal_rate, 'reversal')
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Avg Reversal Success</div>
            <div class="kpi-value">{avg_reversal_rate:.1f}%</div>
            <span class="performance-badge {reversal_class}">{reversal_label}</span>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Market Leader</div>
            <div class="kpi-value" style="font-size: 1.2rem;">{top_performer}</div>
            <div class="kpi-label">{market_share_leader:.1f}% Market Share</div>
        </div>
        """, unsafe_allow_html=True)

    # Performance Analysis Section
    st.markdown("## 📈 Performance Analysis Dashboard")

    # Create tabs for different analysis
    tab1, tab2, tab3, tab4 = st.tabs(["🏆 Volume Leaders", "✅ Success Rates", "⚠️ Risk Analysis", "📊 Performance Matrix"])

    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Top 10 by Volume
            top_volume = filtered_df.nlargest(10, 'Total Volume (In Mn)')
            fig_volume = px.bar(
                top_volume,
                y='UPI Remitter Banks',
                x='Total Volume (In Mn)',
                orientation='h',
                title='Top 10 Banks by Transaction Volume',
                color='Total Volume (In Mn)',
                color_continuous_scale='Blues'
            )
            fig_volume.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig_volume, use_container_width=True)
        
        with col2:
            # Market Share Pie Chart
            fig_pie = px.pie(
                top_volume,
                values='Total Volume (In Mn)',
                names='UPI Remitter Banks',
                title='Market Share Distribution (Top 10)',
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Approval Rate Analysis
            fig_approval = px.bar(
                filtered_df.nlargest(15, 'Approved %'),
                y='UPI Remitter Banks',
                x='Approved %',
                orientation='h',
                title='Top 15 Banks by Approval Rate',
                color='Approved %',
                color_continuous_scale='Greens',
                range_x=[85, 100]
            )
            fig_approval.update_layout(height=600, showlegend=False)
            st.plotly_chart(fig_approval, use_container_width=True)
        
        with col2:
            # Debit Reversal Success
            fig_reversal = px.bar(
                filtered_df.nlargest(15, 'Debit Reversal Success %'),
                y='UPI Remitter Banks',
                x='Debit Reversal Success %',
                orientation='h',
                title='Top 15 Banks by Reversal Success Rate',
                color='Debit Reversal Success %',
                color_continuous_scale='Oranges'
            )
            fig_reversal.update_layout(height=600, showlegend=False)
            st.plotly_chart(fig_reversal, use_container_width=True)

    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Technical Decline Rate (Risk Analysis)
            fig_td = px.bar(
                filtered_df.nlargest(15, 'TD%'),
                y='UPI Remitter Banks',
                x='TD%',
                orientation='h',
                title='Highest Technical Decline Rates (Risk Alert)',
                color='TD%',
                color_continuous_scale='Reds'
            )
            fig_td.update_layout(height=600, showlegend=False)
            st.plotly_chart(fig_td, use_container_width=True)
        
        with col2:
            # Risk Matrix - Low Reversal Success
            low_reversal = filtered_df.nsmallest(15, 'Debit Reversal Success %')
            fig_risk = px.bar(
                low_reversal,
                y='UPI Remitter Banks',
                x='Debit Reversal Success %',
                orientation='h',
                title='Banks with Lowest Reversal Success (Risk Alert)',
                color='Debit Reversal Success %',
                color_continuous_scale='Reds'
            )
            fig_risk.update_layout(height=600, showlegend=False)
            st.plotly_chart(fig_risk, use_container_width=True)

    with tab4:
        # Performance Matrix
        fig_matrix = px.scatter(
            filtered_df,
            x='Approved %',
            y='Debit Reversal Success %',
            size='Total Volume (In Mn)',
            color='TD%',
            hover_name='UPI Remitter Banks',
            title='Performance Matrix: Approval Rate vs Reversal Success',
            color_continuous_scale='RdYlGn_r'
        )
        fig_matrix.update_layout(height=600)
        st.plotly_chart(fig_matrix, use_container_width=True)
        
        # Correlation Analysis
        st.markdown("### 🔗 Performance Correlation Analysis")
        correlation_metrics = ['Total Volume (In Mn)', 'Approved %', 'TD%', 'Debit Reversal Success %']
        corr_df = filtered_df[correlation_metrics].corr()
        
        fig_corr = px.imshow(
            corr_df,
            text_auto=True,
            aspect="auto",
            title="Correlation Matrix of Key Performance Metrics",
            color_continuous_scale='RdBu'
        )
        st.plotly_chart(fig_corr, use_container_width=True)

    # Detailed Performance Table
    st.markdown("## 📋 Detailed Performance Scorecard")

    # Create performance scoring
    def calculate_performance_score(row):
        approval_score = (row['Approved %'] / 100) * 40  # 40% weightage
        td_score = (100 - row['TD%'] * 10) / 100 * 30   # 30% weightage (inverse)
        reversal_score = (row['Debit Reversal Success %'] / 100) * 30  # 30% weightage
        return approval_score + td_score + reversal_score

    filtered_df['Performance Score'] = filtered_df.apply(calculate_performance_score, axis=1)
    filtered_df['Rank'] = filtered_df['Performance Score'].rank(method='dense', ascending=False).astype(int)

    # Sort by performance score
    performance_df = filtered_df.sort_values('Performance Score', ascending=False)

    # Display top performers table
    st.dataframe(
        performance_df[['Rank', 'UPI Remitter Banks', 'Total Volume (In Mn)', 
                    'Approved %', 'TD%', 'Debit Reversal Success %', 'Performance Score']].round(2),
        use_container_width=True
    )
    
if __name__ == "__main__":
    main()