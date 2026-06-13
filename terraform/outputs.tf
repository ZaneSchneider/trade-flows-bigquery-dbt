output "raw_bucket" {
  description = "Name of the raw landing bucket"
  value       = google_storage_bucket.raw.name
}

output "raw_dataset" {
  description = "Raw BigQuery dataset ID"
  value       = google_bigquery_dataset.raw.dataset_id
}