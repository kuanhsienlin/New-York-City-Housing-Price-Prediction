# New-York-City-Housing-Price-Prediction
The goal of this project is to explore the relationship between prices and regional characteristics in the New York City real estate market.

We analyze the relationship between housing prices and factors such as location, nearby facilities, and census tract data of the population. In addition, we use some Machine learning models to make predictions about the housing price by learning and identifying patterns from our datasets. This analysis will help potential real estate buyers understand which factors are important to home prices and help with investment decisions.

In this project, I use below three datasets to do New York City Housing Price Analysis. Analysis objects are mainly divided into two groups: housing of all types and 2b2b  (2 bedrooms and 2 bathrooms) housing. For housing of all types of analysis, we focus on all feature analysis and all types of housing price forecasting. For 2b2b housing analysis, we mainly focus on 2b2b housing median price and census data characteristics of each zipcode area and 2b2b median housing price prediction. We also use maps to show which areas have high and low housing prices for 2b2b housing. Through these analyzes, home buyers and investors can better understand the real estate market and provide a basis for purchasing or investment decisions. People can intuitively understand the level of 2b2b housing prices in different regions, so as to help buyers in the search for their own suitable housing as a reference. At the same time, policymakers can adjust urban planning and housing policies based on geographical analysis.

Below are three datasets sources:

- source1: Web scraping from below Real Estate website
https://www.trulia.com/NY/New_York/{zipcode}/

- source2: Overpass API
https://wiki.openstreetmap.org/wiki/Tag:railway%3Dsubway_entrance

- source3: Web scraping census data from below Unitedstateszipcode websites

 - (1). New York State Zipcode
https://www.unitedstateszipcodes.org/ny/#zips-list

 - (2). Census data for New York City Zipcode
https://www.unitedstateszipcodes.org/{zipcode}/


## Table of contents
### All Types of Housing
* [Set up the environment](#environment)
* [Data Cleaning and Data Transformation](#Data-Cleaning-and-Data-Transformation)
* [Data Combination](#Data-Combination)
* [Feature Derivation and Data Encoding](#Feature-Derivation-and-Data-Encoding)
* [Feature Analysis (Correlation) for All Types of Housing](#Feature-Analysis-(Correlation)-for-All-Types-of-Housing)
* [Machine Learning Models Analysis for Housing Price Prediction](#Machine-Learning-Models-Analysis-for-Housing-Price-Prediction)
* [Conclusion of Machine Learning Models Analysis for Housing Price Prediction](#Conclusion-of-Machine-Learning-Models-Analysis-for-Housing-Price-Prediction)
* [Visualization of Prediction Effect of Random Forest Regression Model](#Visualization-of-Prediction-Effect-of-Random-Forest-Regression-Model)
* [Top 10 Important Features for Housing Price Prediction](#Top-10-Important-Features-for-Housing-Price-Prediction)


### 2b2b Housing
* [Extracting 2b2b Housing Data](#Extracting-2b2b-Housing-Data)
* [Feature Derivation](#Feature-Derivation-2b2b)
* [Data Cleaning](#Data-Cleaning-2b2b)
* [Feature Analysis (Correlation) for 2b2b Housing](#Feature-Analysis-(Correlation)-for-2b2b-Housing)
* [Machine Learning Model Analysis for 2b2b Median Housing Price Prediction](#Machine-Learning-Model-Analysis-for-2b2b-Median-Housing-Price-Prediction)
* [Conclusion of Machine Learning Model Analysis for 2b2b Median Housing Price Prediction](#Conclusion-of-Machine-Learning-Model-Analysis-for-2b2b-Median-Housing-Price-Prediction)
* [2b2b Housing Price Distribution Map](#2b2b-Housing-Price-Distribution-Map)


### Project conclusions
* [Project Conclusions](#Project-Conclusions)
