# Terraform variables for Cloud Run deployment

variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
  default     = ""
}

variable "region" {
  description = "Google Cloud region for Cloud Run service"
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "Name of the Cloud Run service"
  type        = string
  default     = "blood-report-ai"
}

variable "image_name" {
  description = "Docker image name (from Artifact Registry or Docker Hub)"
  type        = string
  default     = "gcr.io/PROJECT_ID/blood-report-ai:latest"
}

variable "memory" {
  description = "Memory allocation for Cloud Run (e.g., '512Mi', '1Gi')"
  type        = string
  default     = "512Mi"
}

variable "cpu" {
  description = "CPU allocation for Cloud Run (e.g., '1', '2')"
  type        = string
  default     = "1"
}

variable "port" {
  description = "Port the application listens on"
  type        = string
  default     = "8000"
}

variable "timeout_seconds" {
  description = "Request timeout in seconds"
  type        = number
  default     = 3600
}

variable "min_instances" {
  description = "Minimum number of instances"
  type        = number
  default     = 0
}

variable "max_instances" {
  description = "Maximum number of instances"
  type        = number
  default     = 100
}

# API Keys - NEVER commit these to Git!
# Use: terraform apply -var="gemini_api_key=YOUR_KEY"
# Or create terraform.tfvars file (add to .gitignore)

variable "gemini_api_key" {
  description = "Google Gemini API Key"
  type        = string
  sensitive   = true
  default     = ""
}

variable "openai_api_key" {
  description = "OpenAI API Key"
  type        = string
  sensitive   = true
  default     = ""
}

variable "anthropic_api_key" {
  description = "Anthropic API Key"
  type        = string
  sensitive   = true
  default     = ""
}

variable "grok_api_key" {
  description = "Grok API Key"
  type        = string
  sensitive   = true
  default     = ""
}
