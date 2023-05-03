<div>
  <img src = "https://cdn.ifsc-climbing.org/images/News/Placeholders/IFSC_News_-_IFSC_placeholder.jpg" width = "800">
</div>

# Using Selenium to Scrape IFSC Website for World Cup Results

The International Federation of Sport Climbing ([IFSC](https://en.wikipedia.org/wiki/International_Federation_of_Sport_Climbing)) was founded in January of 2007 with the goal of being an international governing body for the sport of competition climbing, which consists of the disciplines [lead climbing](https://en.wikipedia.org/wiki/Lead_climbing), [bouldering](https://en.wikipedia.org/wiki/Bouldering), and [speed climbing](https://en.wikipedia.org/wiki/Speed_climbing).
I really love climbing, bouldering in particular, so I figured a project involving climbing would be great for me. I also think web-scraping is insanely useful and really fascinating - though I still have a lot to learn about it.

## What data does this scrape?
This project scrapes ONLY the IFSC World Cup competitions from 2007-present day. Additionally, some events were not able to be scraped because the data is incomplete on the IFSC website (the data format is incorrect, or rounds are missing, or the data literally isn't there). In cases where this occurs, I simply skip that event/category entirely (until I can come up with a reasonable solution at least). For example, sometimes due to weather or other issues, events get postponed, or paritally postponed. This can lead to events such as the World Cup event in Seoul, South Korea 2023, where the rain caused delays and the semi-final round acted as the finals. The results page only lists qualification and semi-final rounds, but currently my code checks for all three rounds. This is a work in progress. The data scraped by my code produces .csv files for each event where each row represents an individual climber and their respective results for the given event.

## Project Goals
* Learn how to use [Selenium](https://www.selenium.dev/) to both scrape the [International Federation of Sport Climbing](https://www.ifsc-climbing.org/) website as well as navigate it
* Exploratory Data Analysis
* Improve/practice my Python programming as well as my data storytelling
* Learn how to use GitHub Pages/Actions to better display the results of the notebook instead of all the code inside
* Learn how to better display and present my notebooks to others (using nbconvert and the aforementioned Actions/Pages)

## Current Status
* Implemented a class to navigate and scrape the [results page](https://www.ifsc-climbing.org/index.php/world-competition/last-result) of the IFSC site
* Stores and tracks all events that have been scraped - creating separate .csv files for each category (Men/Women)
* Additionally scrapes the [IFSC Info](https://ifsc.results.info/#/) page (which is strangely hard to find?) to get the heights of climbers - though only about 10-15% of all climber's heights are actually listed
* Basic analysis for Men's bouldering only
* Merges data into dataframes for some basic analysis
  * Individual climber dataframe
  * Country dataframe
  * Dataframes to identify top climbers by year and by country.
* Scraper class is in its own separate file, and the analysis is also in it's own separate file.
* Have implemented several plotly visualizations to make notebook more interactive
* Added deploy.yml file to set foundation for GitHub Actions & Pages
  * Have very basic action & page setup that converst notebook to html and hosts on [GitHub Page](https://noah-kg.github.io/scraping-IFSC-website-via-selenium/)

## To-Do List
* Implement a more thorough analysis of the data - IN PROGRESS
  - [x] Possibly perform that analysis in a separate notebook?
  - [x] Include competition year in dataframe to allow time-based analysis
  - [x] Distribution of climbers by country
  - [x] Individual finals appearances over time
  - [ ] Add docstrings to all functions

* Work on some static visualizations
  - [ ] Possibly create some Tableau dashboards for more interactivity - MAYBE (focusing on plotly for now)
  - [x] Plotly visualizations
    - [ ] Try to solidify the template, so that it's faster to implement
    - [x] Continuing to learn and add plotly choropleth, bar, line, and heatmap graphs
  - [x] Look into itables to allow search bar for people to look up specific climbers
* Figure out HTML issues so that notebook displays "nicely"
  - [ ] Figure out why static visualizations are getting slightly distorted after html conversion
  - [ ] Identify issue with itables horizontal scrolling (even though there's space)
  - [ ] Set column widths for certain tables to ensure readability
* Add Women's analysis
* Combine Men's & Women's to look at *ALL* climbers simultaneously?
* Possibly learn how to implement [GitHub Actions](https://github.com/features/actions)?
  - [x] Figure out basic foundation for GitHub Actions
