---
title: "Final Project Process"
permalink: /final-project/process/
---

# MovieMap — Where Do the Stories Happen?

Movies, novels, or games often select a real location as their stage if they don't choose to use a fictional one. Screen tourism has also been many people's favorite motivation to visit somewhere. This project presents data storytelling comprising dashboards, interactive maps, and an introduction that show the locations in the United States mentioned in fictional movies and novels, based on datasets from "IMDb Top 250 movies." This project both demonstrates how fictional narratives can co-shape the meaning of a place through data points and provides a practical guide for audiences who plan their travels based on fictional experience.

## Project development

For the project development, I started from collected data from IMDb Top 250. To fit my target of movie location, I further found the database called *Movie-Locations*. At this stage, the major dataset I collected was assembled in an iterative process:

- IMDb Top 250 metadata
- Movie Locations — 91 movie locations
- San Francisco Open Data — *Film Locations in San Francisco*
- Annual Reports of San Francisco (Film SF)
- Hengdian World Studios' representative production list
- Hengdian's attraction shapefile from OpenStreetMap

These datasets were collected and cleaned, aligning with the final goal of building a data storytelling piece in Tableau. I also explored using Three.js in a stack with React and Vite to allow for a smoother experience.

## The final product

The final product is a webpage with three sections:

### 1. From Virtual to Material — how the virtual story shapes the space

In this section, I reported two cases with very different features:

- **San Francisco** is famous for its filming locations, with more than 2,000 movies shot in the city. It uses its existing, natural city space for filming.
- **Hengdian World Studios** in China, on the other hand, is famous for artificial movie spaces built across the entire town, making tourism a core part of the local economy.

### 2. The facts of IMDb movies

In this section, insights from IMDb's Top 250 are explored. The most prominent genre is action, which relies heavily on movie locations. The scatterplot also reveals that movies with higher box office tend to shift from one location type to another.

### 3. The movie-location explorer

In this section, I collected the HTML files and movie posters as the major data for an interactive dashboard. At first, a Tableau dashboard was created, but since interactivity was more desirable, I moved on to Three.js. Since I'm also in a learning process and the time frame was limited, I used Claude Code to assist with the coding and debugging.

## Reflection

The major challenge is to find the most suitable way to exhibit data and connect the dots into a coherent whole. The movie-location topic could easily be thought of as an entertaining project; demonstrating the importance and practical effect of data storytelling has been the real challenge for me.

Given the limited time frame, the project will be further developed and polished for a better effect.