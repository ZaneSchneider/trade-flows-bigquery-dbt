resource "google_storage_bucket" "raw" {
  name     = var.raw_bucket_name
  location = var.region

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = true
}

resource "google_bigquery_dataset" "raw" {
  dataset_id                 = var.raw_dataset_id
  location                   = var.region
  description                = "Raw tables loaded from GCS"
  delete_contents_on_destroy = true
}