# Electric Vehicle Adoption Analysis in Washington State

## Overview

This project analyzes electric vehicle (EV) registration data in Washington State to uncover trends in vehicle types, manufacturers, electric range, and geographic distribution. Using Python for data processing and geospatial visualization, the project generates insights into EV adoption patterns, highlighting urban-rural disparities and market leaders. The analysis is part of a data science portfolio, showcasing proficiency in Python, `pandas`, `geopandas`, `matplotlib`, `seaborn`, and geospatial techniques.

## Dataset

The analysis uses the ["Electric Vehicle Population Data"](https://catalog.data.gov/dataset/electric-vehicle-population-data) from data.gov, containing 223,995 records of EV registrations in Washington State. Key attributes include:
- VIN
- County, City, State
- Model Year, Make, Model
- Electric Vehicle Type (BEV or PHEV)
- Electric Range
- Vehicle Location (latitude/longitude)

The geospatial analysis uses the [U.S. Census Bureau TIGER 2021 county shapefile](https://www2.census.gov/geo/tiger/TIGER2021/COUNTY/), stored locally to map EV registrations to Washington counties.

## Requirements

To run the analysis, install the following Python libraries:
```bash
pip install pandas geopandas matplotlib seaborn shapely us numpy
```

Ensure the following files are available:
- `Electric_Vehicle_Population_Data.csv`: Place in the project root directory.
- `tl_2021_us_county.shp` (and associated files like `.dbf`, `.shx`): Store in a `shapefiles` subdirectory (e.g., `shapefiles/tl_2021_us_county.shp`). Download from the [Census Bureau](https://www2.census.gov/geo/tiger/TIGER2021/COUNTY/) and unzip.

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Prepare the Dataset**:
   - Download `Electric_Vehicle_Population_Data.csv` from [data.gov](https://catalog.data.gov/dataset/electric-vehicle-population-data).
   - Place it in the project root directory.

3. **Prepare the Shapefile**:
   - Download `tl_2021_us_county.zip` from the [Census Bureau](https://www2.census.gov/geo/tiger/TIGER2021/COUNTY/).
   - Unzip to a `shapefiles` subdirectory (e.g., `shapefiles/tl_2021_us_county.shp`).
   - Update the `shp_path` variable in `ev_analysis.py` if your shapefile is in a different location.

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   (Create a `requirements.txt` with the listed libraries if desired.)

## Usage

Run the analysis script:
```bash
python ev_analysis.py
```

The script:
- Loads and cleans the dataset.
- Generates visualizations:
  - Bar charts for EV types, model years, and top manufacturers.
  - Histogram for electric range.
  - Bar chart for top 10 counties by EV registrations.
  - Choropleth map of EV distribution across Washington counties (using a logarithmic scale with annotations for clarity).
- Saves plots as PNG files in the project directory.

## Results

The analysis reveals:
- **EV Types**: Battery Electric Vehicles (BEVs) dominate over Plug-in Hybrid Electric Vehicles (PHEVs).
- **Model Years**: Recent years show a surge in EV registrations.
- **Manufacturers**: Tesla, Nissan, and Chevrolet lead the market.
- **Electric Range**: Most EVs have a range of 100–300 miles.
- **Geographic Distribution**: King County leads in registrations, followed by Snohomish and Pierce. Rural areas lag due to limited charging infrastructure.
- **Choropleth Map**: A logarithmic scale and annotations highlight high-adoption counties like King.

The generated plots (`ev_type_distribution.png`, `ev_model_year.png`, `ev_make_counts.png`, `electric_range.png`, `county_counts.png`, `ev_map.png`) are included in the repository for reference. For a detailed write-up, see the [portfolio article](link-to-your-portfolio-article).

## Repository Structure
```
your-repo-name/
├── ev_analysis.py               # Main analysis script
├── Electric_Vehicle_Population_Data.csv  # Dataset (not included, download from data.gov)
├── shapefiles/                  # Directory for TIGER shapefile (not included, download from Census Bureau)
│   ├── tl_2021_us_county.shp
│   ├── tl_2021_us_county.dbf
│   ├── ...
├── ev_type_distribution.png     # EV type bar chart
├── ev_model_year.png            # Model year bar chart
├── ev_make_counts.png           # Top 10 manufacturers bar chart
├── electric_range.png           # Electric range histogram
├── county_counts.png            # Top 10 counties bar chart
├── ev_map.png                   # Choropleth map
├── README.md                    # This file
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [U.S. Census Bureau](https://www.census.gov/) for the TIGER shapefile.
- [data.gov](https://catalog.data.gov/) for the EV dataset.
- Python libraries: `pandas`, `geopandas`, `matplotlib`, `seaborn`, `shapely`, `us`, `numpy`.