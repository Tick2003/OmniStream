# ==============================================================================
# OMNISTREAM GCP PROJECT & RUNTIME API INITIALIZATION
# ==============================================================================
# This Terraform HCL file automates the creation of a new, secure Google Cloud 
# project, links it to an active billing account, and enables all required 
# service APIs for the OmniStream telemetry and ML recommendation pipeline.

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.10.0"
    }
  }
}

# Variable Definitions for Project Customization
variable "organization_id" {
  type        = string
  description = "The target Google Cloud Organization ID."
  default     = "123456789012" # Replace with actual Organization ID if applicable
}

variable "billing_account_id" {
  type        = string
  description = "The active Google Cloud Billing Account ID."
  default     = "012345-67890A-BCDEF0" # Replace with actual Billing ID
}

variable "project_name" {
  type        = string
  description = "Display name of the GCP project."
  default     = "OmniStream AI Solutions PoC"
}

variable "project_id" {
  type        = string
  description = "Unique immutable global identifier for the new GCP project."
  default     = "omnistream-ai-poc-prod"
}

# 1. Project Creation Resource
resource "google_project" "omnistream_project" {
  name            = var.project_name
  project_id      = var.project_id
  org_id          = var.organization_id
  billing_account = var.billing_account_id
  
  # Prevents accidental deletion of the project in production environments
  lifecycle {
    prevent_destroy = false
  }

  labels = {
    project_tier = "proof-of-concept"
    department   = "ai-solutions"
    owner        = "solutions-architect-team"
  }
}

# 2. Automated API Enablement Service Blocks
# In GCP, services must be explicitly activated before resources can be provisioned.
resource "google_project_service" "enabled_apis" {
  for_each = toset([
    "compute.googleapis.com",         # Compute Engine (Required for Dataflow workers)
    "pubsub.googleapis.com",          # Pub/Sub (Real-time clickstream ingestion queue)
    "dataflow.googleapis.com",        # Dataflow (Stream processing engine)
    "bigquery.googleapis.com",        # BigQuery (Data warehouse analytical storage)
    "aiplatform.googleapis.com",      # Vertex AI (Model training and vector serving)
    "storage.googleapis.com",         # Cloud Storage (Model storage and data staging)
    "iam.googleapis.com",             # IAM API (Service Account management)
    "cloudkms.googleapis.com"         # Cloud KMS (Customer-Managed Encryption Keys)
  ])

  project                    = google_project.omnistream_project.project_id
  service                    = each.key
  disable_dependent_services = true
  disable_on_destroy         = true

  depends_on = [google_project.omnistream_project]
}

# 3. Base Storage Bucket for Vertex AI Pipeline Staging & Templates
resource "google_storage_bucket" "pipeline_staging_bucket" {
  name                        = "${google_project.omnistream_project.project_id}-staging-bucket"
  project                     = google_project.omnistream_project.project_id
  location                    = "US" # Multi-regional resilience
  force_destroy               = true
  public_access_prevention    = "enforced"
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  depends_on = [google_project_service.enabled_apis]
}

# Output Block showing successfully generated details
output "gcp_project_details" {
  value = {
    project_name       = google_project.omnistream_project.name
    project_id         = google_project.omnistream_project.project_id
    project_number     = google_project.omnistream_project.number
    staging_bucket_url = google_storage_bucket.pipeline_staging_bucket.url
  }
  description = "Properties of the newly provisioned Google Cloud Project environment."
}
