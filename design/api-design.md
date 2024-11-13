# API design

## Requirements

* API should be relatively easy to call (i.e., through a single GET request)
* It should be reasonably responsive by default (<5s)
* API returns JSON object
* If the schema is expected to change a lot, versioned API routes would be preferable.

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
