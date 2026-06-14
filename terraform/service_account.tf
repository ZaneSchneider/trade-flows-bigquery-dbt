# Runtime identity the BACI fetcher authenticates as
resource "google_service_account" "fetcher" {
  account_id   = "baci-fetcher"
  display_name = "BACI fetcher (runtime GCS upload)"
}

# Least privilege: objectAdmin on ONLY the raw bucket — not project-wide
resource "google_storage_bucket_iam_member" "fetcher_raw" {
  bucket = google_storage_bucket.raw.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.fetcher.email}"
}