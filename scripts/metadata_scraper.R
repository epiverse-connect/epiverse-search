package_metadata <- httr2::request("https://epiverse-connect.r-universe.dev/api/packages") |>
  httr2::req_user_agent("R-universe docs") |>
  httr2::req_perform() |>
  httr2::resp_body_json()

pkg_metadata_api <- package_metadata |>
  purrr::map(~ unlist(.x[c("Package", "Title", "URL", "RemoteUrl", "_pkglogo")])) |>
  dplyr::bind_rows() |>
  dplyr::mutate(
    URL_list = stringr::str_split(URL, "[,\\n[:space:]]+"),
    # First URL that doesn't look like a link to a GitHub repo
    docs_URL = purrr::map(URL_list, ~ .x[match(FALSE, startsWith(.x, "https://github.com"))])
  ) |>
  dplyr::select(
    # Names expected by the front end
    package = Package,
    logo = "_pkglogo",
    website = docs_URL,
    source = RemoteUrl
    # TODO: Add vignettes
  )

