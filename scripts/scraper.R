library(pkgsearch)
library(gh)
pak::pak("Genentech/rd2markdown")
## Helper function to ensure dirs exist
write_content_to_file <- function(content, file_path, is_binary = FALSE) {
  # Write the content to the file while checking for binaryness
  if (!is_binary) {
    dir_path <- dirname(file_path)
    # If dir doesn't exist, create it
    if (!dir.exists(dir_path)) {
      dir.create(dir_path, recursive = TRUE)
    }
    writeLines(rawToChar(content), file_path)
  }
}

# Helper function to determine if file extension indicates binary
is_binary_file <- function(file_path) {
  binary_extensions <- c(
    "png",
    "jpg",
    "jpeg",
    "gif",
    "pdf",
    "zip",
    "tar",
    "gz",
    "bz2",
    "xz",
    "exe",
    "dll",
    "bin"
  )
  file_ext <- tools::file_ext(file_path)
  return(file_ext %in% binary_extensions)
}

# Define the URL and output file path
ctv_url <- "https://raw.githubusercontent.com/cran-task-views/Epidemiology/main/Epidemiology.md"
output_file <- "Epidemiology.md"

# Download the file from the URL and save it to the specified path
download.file(ctv_url, output_file)

# Read the CTV file and extract package names
pkgs <- ctv::read.ctv("Epidemiology.md") |>
  purrr::pluck("packagelist", "name") |>
  tail(3)

owner <- "cran"

# Vectorized approach to get title and description of each package
lapply(pkgs, FUN = function(pkg) {
  # Use the gh function to list all files in the repository
  files <- gh::gh(
    "GET /repos/:owner/:repo/git/trees/HEAD?recursive=1",
    owner = owner,
    repo = pkg
  )

  # Extract the file paths
  file_paths <- vapply(files$tree, function(x) x$path, character(1))

  # Find the file that matches the target path
  matched_regex <- grep(file_paths, pattern = "^(man/|vignettes/)")
  matching_files <- file_paths[matched_regex]

  # If matching files are found, download content of each file
  if (length(matching_files) > 0) {
    filteredFiles <- Filter(function(x) x$type == "blob", files$tree[matched_regex])
    lapply(filteredFiles, FUN = function(file) {
      target_path <- sprintf("sources/%s/%s", pkg, file$path)

      # Use the gh function to get the blob content
      blob <- gh::gh(
        "GET /repos/:owner/:repo/git/blobs/:sha",
        owner = owner,
        repo = pkg,
        sha = file$sha
      )

      # Decode the base64 content
      file_content <- base64enc::base64decode(blob$content)

      # Determine if the file should be written as binary
      is_binary <- is_binary_file(target_path)

      # Save the .Rd content to a file with our helper function
      # The helper ensures the paths exist prior to saving
      tryCatch(write_content_to_file(file_content, target_path, is_binary),
        error = function(e) {
          cat("Error downloading or saving file:", target_path, "\n")
          cat("Error message:", e$message, "\n")
        }
      )

      if (!is_binary && grepl("\\.Rd$", target_path, ignore.case = TRUE)) {
        # Convert Rd to markdown
        rd <- rd2markdown::get_rd(file = target_path)
        writeLines(
          rd2markdown::rd2markdown(rd),
          gsub("\\.Rd$", ".md", target_path) # Replace the extension name
        )
        # Remove the original Rd file
        tryCatch(unlink(target_path),
          error = function(e) {
            cat("Error removing file:", target_path, "\n")
            cat("Error message:", e$message, "\n")
          }
        )
      }

      cat("File downloaded and saved as", target_path, "\n")
    })
  } else {
    cat("No matching file found for package:", pkg, "\n")
  }
})

# Define the path to the sources/package/ directory
sources_package_path <- "sources"

# List all subdirectories within sources/package/
packages <- list.dirs(sources_package_path, full.names = TRUE, recursive = FALSE)

# Iterate over each package directory
for (pkg in packages) {
  man_path <- file.path(pkg, "man")

  # Check if the man/ directory exists
  if (dir.exists(man_path)) {
    # List all subdirectories within man/
    man_subdirs <- list.dirs(man_path, full.names = TRUE, recursive = FALSE)

    # Remove each subdirectory within man/
    for (subdir in man_subdirs) {
      unlink(subdir, recursive = TRUE)
    }
  }
}
