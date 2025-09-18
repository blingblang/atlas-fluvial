terraform {
  required_version = ">= 1.0"

  required_providers {
    vercel = {
      source  = "vercel/vercel"
      version = "~> 1.0"
    }
  }
}

# Configure the Vercel Provider
provider "vercel" {
  # api_token = var.vercel_api_token # Set via VERCEL_API_TOKEN environment variable
}

# Variables
variable "project_name" {
  description = "Name of the Vercel project"
  type        = string
  default     = "atlas-fluvial"
}

variable "github_repo" {
  description = "GitHub repository (format: owner/repo)"
  type        = string
  default     = "blingblang/atlas-fluvial"
}

variable "production_branch" {
  description = "Git branch for production deployments"
  type        = string
  default     = "main"
}

# Vercel Project
resource "vercel_project" "atlas_fluvial" {
  name      = var.project_name
  framework = "nextjs"

  git_repository = {
    type = "github"
    repo = var.github_repo
  }

  root_directory = "atlasfluvial-site"

  build_command    = "npm install && npm run build"
  output_directory = "out"
  install_command  = "npm install"
  dev_command      = "npm run dev"

  environment = [
    {
      key    = "NODE_VERSION"
      value  = "18"
      target = ["production", "preview", "development"]
    }
  ]
}

# Domain configuration (optional - uncomment and configure if you have a custom domain)
# resource "vercel_project_domain" "atlas_fluvial_domain" {
#   project_id = vercel_project.atlas_fluvial.id
#   domain     = "atlas-fluvial.com"  # Replace with your actual domain
# }

# Outputs
output "project_id" {
  description = "The ID of the Vercel project"
  value       = vercel_project.atlas_fluvial.id
}

output "production_url" {
  description = "The production URL of the deployed application"
  value       = "https://${var.project_name}.vercel.app"
}