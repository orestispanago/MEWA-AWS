# MEWA-AWS

Download rain and climate records from MEWA REST API.

Scripts:
* `rain.py` downloads rain data using this naming format:
`data/rain/rain_YYYYmm.csv`

* `weather.py` downloads climate records in this format: 
`data/weather/YYYY/weather_YYYYmmdd.csv`

* `processing.py` reads monthly files and summarizes data periods for each station at `data/rain_summary.csv`

* `plotting.py` plots pie chart with station types, map with station locations, types and number of values.

Shapefiles downloaded from https://gadm.org/download_country.html

