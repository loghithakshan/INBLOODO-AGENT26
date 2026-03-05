# Terraform configuration for Google Cloud Run deployment
# Deploy with: terraform apply

terraform {
  required_version = ">= 0.12"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "required_apis" {
  for_each = toset([
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "artifactregistry.googleapis.com"
  ])
  
  service            = each.value
  disable_on_destroy = false
}

# Cloud Run Service
resource "google_cloud_run_service" "blood_report_ai" {
  name     = var.service_name
  location = var.region
  
  depends_on = [google_project_service.required_apis]
  
  template {
    spec {
      service_account_name = google_service_account.blood_report_ai.email
      
      containers {
        image = var.image_name
        
        ports {
          container_port = var.port
        }
        
        resources {
          limits = {
            memory = var.memory
            cpu    = var.cpu
          }
        }
        
        env {
          name  = "GEMINI_API_KEY"
          value = var.gemini_api_key
        }
        
        env {
          name  = "OPENAI_API_KEY"
          value = var.openai_api_key
        }
        
        env {
          name  = "ANTHROPIC_API_KEY"
          value = var.anthropic_api_key
        }
        
        env {
          name  = "GROK_API_KEY"
          value = var.grok_api_key
        }
        
        env {
          name  = "HOST"
          value = "0.0.0.0"
        }
        
        env {
          name  = "PORT"
          value = var.port
        }
        
        env {
          name  = "DEBUG"
          value = "false"
        }
      }
      
      timeout_seconds = var.timeout_seconds
    }
    
    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale" = var.max_instances.toString()
        "autoscaling.knative.dev/minScale" = var.min_instances.toString()
      }
    }
  }
  
  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Allow unauthenticated access
resource "google_cloud_run_service_iam_member" "noauth" {
  service  = google_cloud_run_service.blood_report_ai.name
  location = var.region
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Service Account
resource "google_service_account" "blood_report_ai" {
  account_id   = "blood-report-ai"
  display_name = "Blood Report AI Service Account"
}

# Grant service account necessary roles
resource "google_project_iam_member" "logging" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.blood_report_ai.email}"
}

resource "google_project_iam_member" "monitoring" {
  project = var.project_id
  role    = "roles/monitoring.metricWriter"
  member  = "serviceAccount:${google_service_account.blood_report_ai.email}"
}

# Outputs
output "service_url" {
  description = "The URL of the deployed Cloud Run service"
  value       = google_cloud_run_service.blood_report_ai.status[0].url
}

output "service_name" {
  description = "The name of the Cloud Run service"
  value       = google_cloud_run_service.blood_report_ai.name
}

output "region" {
  description = "The region where the service is deployed"
  value       = var.region
}
