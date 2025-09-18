# Terraform Configuration for Atlas Fluvial

This directory contains the Terraform configuration for deploying the Atlas Fluvial application to Vercel.

## Prerequisites

1. Install Terraform (version 1.0 or later)
2. Install Vercel CLI: `npm i -g vercel`
3. Create a Vercel account and obtain an API token from https://vercel.com/account/tokens

## Setup

1. Copy the example variables file:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

2. Edit `terraform.tfvars` with your project-specific values.

3. Set your Vercel API token as an environment variable:
   ```bash
   export VERCEL_API_TOKEN="your-vercel-api-token"
   ```

## Deployment

1. Initialize Terraform:
   ```bash
   terraform init
   ```

2. Review the planned changes:
   ```bash
   terraform plan
   ```

3. Apply the configuration:
   ```bash
   terraform apply
   ```

## Managing Infrastructure

- To update the infrastructure: Make changes to the `.tf` files and run `terraform apply`
- To destroy the infrastructure: `terraform destroy`
- To view current state: `terraform show`

## Environment Variables

The following environment variables can be configured in the Vercel dashboard or through Terraform:

- `NODE_VERSION`: Node.js version for the build environment (default: 18)
- Additional application-specific environment variables can be added in `main.tf`

## Custom Domain

To configure a custom domain, uncomment and configure the `vercel_project_domain` resource in `main.tf`.

## CI/CD Integration

The Vercel project is configured to automatically deploy:
- Production deployments from the `main` branch
- Preview deployments from pull requests

## Troubleshooting

If you encounter issues:

1. Ensure your Vercel API token is correctly set
2. Verify the GitHub repository access permissions
3. Check Terraform logs for detailed error messages
4. Visit the Vercel dashboard for deployment logs

## Resources

- [Vercel Terraform Provider Documentation](https://registry.terraform.io/providers/vercel/vercel/latest/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [Terraform Documentation](https://www.terraform.io/docs)