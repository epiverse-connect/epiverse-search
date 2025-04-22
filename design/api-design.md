# API design

## Requirements

* API should be relatively easy to call (i.e., through a single GET request)
* It should be reasonably responsive by default (<5s)
* API returns JSON object
* If the schema is expected to change a lot, versioned API routes would be preferable.
* Results are ordered by score by the backend and returned as ordered in the API answer

## Querying the API

API calls are contained to one call per query. Front-end calls could look like `api.epiverse.org/query="how to estimate outbreak probability of dengue in colombia in next three months"&filter="epiverse"` (versioned could look like `api.epiverse.org/v1/query[...]`).

## Response

```json
{
  "query": "how to estimate outbreak probability of dengue in colombia in next three months",
  "filter": "epiverse",
  "response": {
    "results": [
      {
        "package": "epidemics",
        "title": "Composable epidemic scenario modelling",
        "description": "A library of compartmental epidemic models taken from the published literature, and classes to represent affected populations, public health response measures including non-pharmaceutical interventions on social contacts, non-pharmaceutical and pharmaceutical interventions that affect disease transmissibility, vaccination regimes, and disease seasonality, which can be combined to compose epidemic scenario models.",
        "logo": "https://epiverse-trace.github.io/epidemics/logo.svg",
        "website": "https://epiverse-trace.github.io/epidemics",
        "source": "https://github.com/epiverse-trace/epidemics",
        "vignettes": [
            "https://epiverse-trace.github.io/epidemics/articles/modelling_interventions.html",
            "https://epiverse-trace.github.io/epidemics/articles/modelling_multiple_interventions.html"
        ],
        "relevance": 0.987
      },
      {
        "package": "finalsize",
        "title": "Calculate the Final Size of an Epidemic",
        "description": "Calculate the final size of a susceptible-infectious-recovered epidemic in a population with demographic variation in contact patterns and susceptibility to disease, as discussed in Miller (2012)",
        "logo": "https://epiverse-trace.github.io/finalsize/logo.svg",
        "website": "https://epiverse-trace.github.io/finalsize",
        "source": "https://github.com/epiverse-trace/finalsize",
        "vignettes": [
            "<url>"
        ],
        "relevance": 0.643
      }
    ]
  }
}
```
