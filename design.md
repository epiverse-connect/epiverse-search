# Epiverse search

## User persona & user story

This work is mostly targeted at the following persona, with the following stories:

- As a PEI tool implementer, I want to find out if there is an R package to do this specific epidemiological analysis task I have in mind.
- As a PEI tool creator, I want to find out if there

These user stories have been collected at:

- the '100 days and 100 lines of code' workshop (December 2022)
- the 'Solution for Collaboratory' launch workshop (January 2023)

## Requirements

The search functionality should:

- take natural language text description of the task the user is trying to perform (e.g., "I want to estimate the risk of a dengue outbreak in Colombia in the next 3 months")
- return a (list of) valid R package(s) performing the described task, taken from the CRAN Task View in Epidemiology 

The search functionality should NOT:

- return hallucinated non-existing R packages
- return stochastic results. The same query on the same version of the engine should return the same results

## Deployment

This will be part of the https://epiverse-trace.github.io/ website.

## Out of scope

- The search results are based EXCLUSIVELY on match to the described task. Software quality is not taken into account in result rankings

