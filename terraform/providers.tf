terraform {
  backend "gcs" {
    bucket = "your-bucket-name"
    prefix = "terraform-state"
  }

  required_providers {
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.2.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 4.44.1"
    }
  }
}