import plotly.express as px
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
import pandas as pd


def generate_interactive_charts_and_map(dataframe):
    # Store paths of all charts
    chart_paths = []

    # Chart 5: Crime location distribution map (Folium)
    map_center = [dataframe["Latitude"].mean(), dataframe["Longitude"].mean()]
    crime_map = folium.Map(location=map_center, zoom_start=13)
    marker_cluster = MarkerCluster().add_to(crime_map)

    for _, row in dataframe.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=f"Crime: {row['CrimeCode']}<br>Location: {row['Location']}<br>Date: {row['CrimeDateTime']}",
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(marker_cluster)

    map_path = "static/crime_map.html"
    crime_map.save(map_path)  # Save map as an HTML file
    chart_paths.append({"path": map_path, "title": "Crime Map"})

    # Chart 1: Crime type distribution
    # Count the number of cases for each CrimeCode
    crime_category_counts = (
        dataframe.groupby(["CrimeCode", "Description"]).size().reset_index(name="Count")
    )
    # Create an interactive bar chart
    fig1 = px.bar(
        crime_category_counts,
        x="CrimeCode",
        y="Count",
        title="Crime Count by Category",
        labels={"CrimeCode": "Crime Code", "Count": "Count"},
        color="Count",  # Color by crime count
        color_continuous_scale="Darkmint",  # Use continuous color scale
        hover_data={
            "Description": True,
            "CrimeCode": True,
            "Count": True,
        },  # Add hover data
    )
    # Beautify the chart
    fig1.update_traces(
        marker=dict(line=dict(color="black", width=1)),  # Add border to bars
        hoverlabel=dict(
            bgcolor="white", font_size=14, font_family="Arial"
        ),  # Hover label style
    )
    fig1.update_layout(
        title=dict(
            text="Crime Count by Category",
            font=dict(size=24, color="darkblue", family="Arial"),
            x=0.5,  # Center title
        ),
        xaxis=dict(
            title=dict(text="Crime Code", font=dict(size=18, color="darkblue")),
            tickfont=dict(size=14, color="black"),
            showgrid=True,
            gridcolor="lightgrey",
            linecolor="black",
        ),
        yaxis=dict(
            title=dict(text="Count", font=dict(size=18, color="darkblue")),
            tickfont=dict(size=14, color="black"),
            showgrid=True,
            gridcolor="lightgrey",
            rangemode="tozero",
        ),
        plot_bgcolor="white",  # White background for chart
        paper_bgcolor="white",  # White background for outer frame
        margin=dict(l=50, r=50, t=100, b=50),  # Adjust margins
        font=dict(family="Arial", size=12, color="black"),
        coloraxis_showscale=True,  # Show color scale
    )
    # Set the color scale direction (darker color indicates higher count)
    fig1.update_coloraxes(reversescale=False)
    # Remove legend for CrimeCode
    fig1.update_layout(showlegend=False)
    # Show the chart
    chart1_path = "static/crime_count_by_category.html"
    fig1.write_html(chart1_path)
    chart_paths.append({"path": chart1_path, "title": "Crime Count by Category"})

    # Chart 2: Crime type by gender distribution
    # Count by gender and crime code
    gender_crime_counts = (
        dataframe.groupby(["Gender", "CrimeCode", "Description"])
        .size()
        .reset_index(name="Count")
    )
    # Replace gender codes with full names
    gender_crime_counts["Gender"] = gender_crime_counts["Gender"].replace(
        {"M": "Male", "F": "Female", "U": "Unknown"}
    )
    # Define full CrimeCode order
    all_crime_codes = sorted(dataframe["CrimeCode"].unique())
    all_genders = ["Male", "Female", "Unknown"]
    # Create full combinations
    full_combinations = pd.MultiIndex.from_product(
        [all_crime_codes, all_genders], names=["CrimeCode", "Gender"]
    )
    gender_crime_counts = (
        gender_crime_counts.set_index(["CrimeCode", "Gender"])
        .reindex(full_combinations, fill_value=0)
        .reset_index()
    )
    # Restore Description column
    description_mapping = (
        dataframe.set_index("CrimeCode")["Description"].drop_duplicates().to_dict()
    )
    gender_crime_counts["Description"] = gender_crime_counts["CrimeCode"].map(
        description_mapping
    )
    # Ensure CrimeCode is displayed in order
    gender_crime_counts["CrimeCode"] = pd.Categorical(
        gender_crime_counts["CrimeCode"], categories=all_crime_codes, ordered=True
    )
    # Create an interactive grouped bar chart
    fig2 = px.bar(
        gender_crime_counts,
        x="CrimeCode",
        y="Count",
        color="Gender",  # Group by gender
        barmode="group",  # Grouped bar chart
        title="Crime Count by Gender and Crime Code",
        labels={"CrimeCode": "Crime Code", "Count": "Count"},  # Modify X-axis label
        hover_data={
            "Description": True,
            "Count": True,
            "Gender": True,
        },  # Add Description to hover data
        color_discrete_map={
            "Male": "lightblue",
            "Female": "orange",
            "Unknown": "gray",
        },  # Custom gender colors
    )
    # Beautify the chart
    fig2.update_traces(
        hoverlabel=dict(
            bgcolor="white", font_size=14, font_family="Arial"
        ),  # Hover label style
        marker=dict(line=dict(color="black", width=0.8)),  # Bar border
    )
    fig2.update_layout(
        title=dict(
            text="Crime Count by Gender and Crime Code",
            font=dict(size=20, color="darkblue", family="Arial"),
            x=0.5,  # Center title
        ),
        xaxis=dict(
            title="Crime Code",
            tickfont=dict(size=14, color="black"),
            showgrid=False,  # Hide vertical grid lines
            linecolor="black",  # X-axis line color
        ),
        yaxis=dict(
            title="Count",
            tickfont=dict(size=14, color="black"),
            gridcolor="lightgrey",  # Horizontal grid line color
        ),
        plot_bgcolor="white",  # White background
        font=dict(family="Arial", size=12, color="black"),
        legend=dict(
            title=dict(text="Gender", font=dict(size=14, color="black")),
            font=dict(size=12, color="black"),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
        ),
        hovermode="closest",  # Show hover label for each bar
    )
    # Show the chart
    chart2_path = "static/crime_count_by_gender_and_crime_code.html"
    fig2.write_html(chart2_path)
    chart_paths.append({"path": chart2_path, "title": "Count by Gender and Crime Code"})

    # Chart 3: Crime record distribution by time
    # Prepare data
    daily_crime_counts = (
        dataframe.groupby(dataframe["CrimeDateTime"].dt.date)
        .size()
        .reset_index(name="CrimeCount")
    )
    daily_crime_counts.columns = ["Date", "CrimeCount"]
    # Use Plotly to draw a line chart
    fig3 = px.line(
        daily_crime_counts,
        x="Date",
        y="CrimeCount",
        title="Daily Crime Counts",
        labels={"Date": "Date", "CrimeCount": "Crime Count"},
        markers=True,
    )
    # Beautify the chart
    fig3.update_traces(
        line=dict(color="royalblue", width=3),
        marker=dict(
            size=8, symbol="circle", color="orange", line=dict(color="black", width=1)
        ),
    )
    fig3.update_layout(
        title=dict(
            text="Daily Crime Counts",
            font=dict(size=24, color="darkblue"),
            x=0.5,  # Center title
        ),
        xaxis=dict(
            title=dict(text="Date", font=dict(size=18, color="darkblue")),
            tickfont=dict(size=14, color="black"),
            showgrid=True,
            gridcolor="lightgrey",
            linecolor="black",
        ),
        yaxis=dict(
            title=dict(text="Crime Count", font=dict(size=18, color="darkblue")),
            tickfont=dict(size=14, color="black"),
            showgrid=True,
            gridcolor="lightgrey",
            rangemode="tozero",
        ),
        plot_bgcolor="white",  # White background
        hovermode="x unified",  # Unified hover for all data points
        font=dict(family="Arial", size=12, color="black"),
    )
    # Show the chart
    chart3_path = "static/daily_crime_counts.html"
    fig3.write_html(chart3_path)
    chart_paths.append({"path": chart3_path, "title": "Daily Crime Counts"})

    # Chart 4: Crime distribution by age group
    # Define age intervals and labels
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    labels = [
        "0-10",
        "11-20",
        "21-30",
        "31-40",
        "41-50",
        "51-60",
        "61-70",
        "71-80",
        "81-90",
    ]
    # Group ages
    dataframe["AgeGroup"] = pd.cut(
        pd.to_numeric(dataframe["Age"], errors="coerce"),
        bins=bins,
        labels=labels,
        right=False,
    )
    # Expand 'AgeGroup' column to include 'U' for unknown
    dataframe["AgeGroup"] = dataframe["AgeGroup"].astype("category")
    dataframe["AgeGroup"] = dataframe["AgeGroup"].cat.add_categories("U")
    # Prepare data
    age_group_counts = dataframe["AgeGroup"].value_counts().sort_index().reset_index()
    age_group_counts.columns = ["AgeGroup", "Count"]
    # Create an interactive bar chart
    fig4 = px.bar(
        age_group_counts,
        x="AgeGroup",
        y="Count",
        title="Crime Distribution by Age Groups (Including Unknown)",
        labels={"AgeGroup": "Age Group", "Count": "Count"},
        color="Count",  # Color by count
        color_continuous_scale="Blues",  # Gradient color: darker means more counts
    )
    # Beautify the chart
    fig4.update_traces(
        marker=dict(line=dict(color="black", width=1)),  # Add border to bars
        hovertemplate="<b>Age Group:</b> %{x}<br><b>Count:</b> %{y}",  # Custom hover template
    )
    fig4.update_layout(
        title=dict(
            text="Crime Distribution by Age Groups (Including Unknown)",
            font=dict(size=24, color="darkblue"),
            x=0.5,  # Center title
        ),
        xaxis=dict(
            title="Age Group", tickfont=dict(size=14, color="black"), linecolor="black"
        ),
        yaxis=dict(
            title="Count", tickfont=dict(size=14, color="black"), gridcolor="lightgrey"
        ),
        plot_bgcolor="white",  # White background
        font=dict(family="Arial", size=12, color="black"),
        coloraxis_showscale=True,  # Show color scale
    )
    # Show the chart
    chart4_path = "static/crime_distribution_by_age_groups.html"
    fig4.write_html(chart4_path)
    chart_paths.append(
        {
            "path": chart4_path,
            "title": "Crime Distribution by Age Groups (Including Unknown)",
        }
    )
    return chart_paths

def generate_interactive_new_charts(data):
    chart_paths_2 = []

    # Chart 5
    # Count the number of crimes per weather condition
    weather_crime_counts = data["weather_description"].value_counts().reset_index()
    weather_crime_counts.columns = ["Weather Condition", "Number of Crimes"]
    # Create an interactive bar chart using Plotly
    fig5 = px.bar(
        weather_crime_counts,
        x="Weather Condition",
        y="Number of Crimes",
        color="Number of Crimes",
        color_continuous_scale="Haline",
        title="Crime Frequency by Weather Condition",
        labels={
            "Number of Crimes": "Number of Crimes",
            "Weather Condition": "Weather Condition",
        },
        template="plotly_white",
    )
    # Customize chart layout
    fig5.update_layout(
        xaxis=dict(title="Weather Condition", tickangle=45, linecolor="black"),
        yaxis=dict(title="Number of Crimes"),
        title=dict(font=dict(size=20), x=0.5),  # Center the title
        coloraxis_colorbar=dict(title="Crime Count"),
        margin=dict(l=40, r=40, t=40, b=40),
    )
    # Save the interactive chart as an HTML file
    chart5_path = "static/crime_frequency_by_weather_condition.html"
    fig5.write_html(chart5_path)
    chart_paths_2.append(
        {
            "path": chart5_path,
            "title": "Crime Frequency by Weather Condition",
        }
    )

    # Chart 6
    # Load the crime-weather merged dataset
    # Convert the CrimeDateTime column to datetime format
    data["CrimeDateTime"] = pd.to_datetime(data["CrimeDateTime"])
    # Extract the hour of the day
    data["Hour"] = data["CrimeDateTime"].dt.hour
    # Group by hour and weather description, and count occurrences
    hourly_weather_crime = (
        data.groupby(["Hour", "weather_description"])
        .size()
        .reset_index(name="Crime Count")
    )
    # Create an interactive area chart using Plotly
    fig6 = px.area(
        hourly_weather_crime,
        x="Hour",
        y="Crime Count",
        color="weather_description",
        title="Crime Distribution by Hour and Weather Condition",
        labels={
            "Hour": "Hour of the Day",
            "Crime Count": "Number of Crimes",
            "weather_description": "Weather Condition",
        },
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )
    # Customize layout: Center the title and add X-axis gridlines
    fig6.update_layout(
        xaxis=dict(
            title="Hour of the Day",
            tickmode="linear",
            dtick=1,
            showgrid=True,  # Enable gridlines for the X-axis
            gridcolor="lightgrey",  # Set gridline color
        ),
        yaxis=dict(title="Number of Crimes", showgrid=True),
        title=dict(
            text="Crime Distribution by Hour and Weather Condition",
            font=dict(size=20),
            x=0.5,  # Center the title
            xanchor="center",
        ),
        legend_title=dict(text="Weather Condition"),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified",
    )
    # Save the interactive chart as an HTML file
    chart6_path = "static/crime_by_hour_weather_interactive.html"
    fig6.write_html(chart6_path)
    chart_paths_2.append(
        {
            "path": chart6_path,
            "title": "Crime Distribution by Hour and Weather Condition",
        }
    )

    return chart_paths_2
