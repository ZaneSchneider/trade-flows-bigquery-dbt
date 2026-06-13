variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "Region for the bucket and BigQuery dataset — must match for GCS->BQ loads"
  type        = string
  default     = "us-west1"
}

variable "raw_bucket_name" {
  description = "GCS bucket for landing raw files"
  type        = string
}

variable "raw_dataset_id" {
  description = "BigQuery dataset for raw loaded tables"
  type        = string
}