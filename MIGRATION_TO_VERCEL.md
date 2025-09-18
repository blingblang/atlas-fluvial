# Migration from Netlify to Vercel

This document outlines the changes made to migrate the Atlas Fluvial project from Netlify to Vercel deployment.

## Overview

The project has been successfully migrated from Netlify to Vercel, including:
- Static site deployment configuration
- Terraform infrastructure as code
- File upload functionality (from Netlify CDN to Vercel Blob Storage)
- Deployment scripts and automation

## Changes Made

### 1. Deployment Configuration

#### Added Files:
- `atlasfluvial-site/vercel.json` - Vercel deployment configuration
- `atlasfluvial-site/deploy_vercel.py` - Python script for Vercel deployment
- `terraform/main.tf` - Terraform configuration for Vercel infrastructure
- `terraform/terraform.tfvars.example` - Example Terraform variables
- `terraform/README.md` - Terraform documentation

#### Retained for Reference:
- `atlasfluvial-site/netlify.toml` - Can be removed after confirming Vercel deployment works
- `atlasfluvial-site/deploy.py` - Original Netlify deployment script (can be removed)

### 2. File Upload Migration

#### Added:
- `src/pdf_generator/vercel_uploader.py` - New Vercel Blob Storage uploader

#### Updated:
- `src/pdf_generator/agent.py` - Changed from `netlify_uploader` to `vercel_uploader`

#### Retained for Reference:
- `src/pdf_generator/netlify_uploader.py` - Can be removed after testing

### 3. Environment Variables

New environment variables required:
```bash
# Vercel deployment and storage
VERCEL_TOKEN=your_vercel_api_token
BLOB_READ_WRITE_TOKEN=your_vercel_blob_storage_token
```

Old Netlify variables (can be removed):
```bash
NETLIFY_SITE_ID=...
NETLIFY_ACCESS_TOKEN=...
```

## Setup Instructions

### 1. Vercel Account Setup

1. Create a Vercel account at https://vercel.com
2. Generate an API token from https://vercel.com/account/tokens
3. Enable Blob Storage in your Vercel dashboard

### 2. Local Development

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Set environment variables:
   ```bash
   export VERCEL_TOKEN=your_vercel_api_token
   export BLOB_READ_WRITE_TOKEN=your_blob_storage_token
   ```

3. Deploy to Vercel:
   ```bash
   cd atlasfluvial-site
   python deploy_vercel.py         # For preview deployment
   python deploy_vercel.py --prod  # For production deployment
   ```

### 3. Terraform Deployment

1. Navigate to terraform directory:
   ```bash
   cd terraform
   ```

2. Initialize Terraform:
   ```bash
   terraform init
   ```

3. Configure variables:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your settings
   ```

4. Deploy infrastructure:
   ```bash
   terraform plan
   terraform apply
   ```

## Features Comparison

| Feature | Netlify | Vercel |
|---------|---------|---------|
| Static Site Hosting | ✅ | ✅ |
| Automatic Git Deploys | ✅ | ✅ |
| Preview Deployments | ✅ | ✅ |
| Custom Headers | ✅ | ✅ |
| Redirects | ✅ | ✅ |
| File Storage | Netlify CDN | Vercel Blob Storage |
| Infrastructure as Code | ❌ | ✅ (Terraform) |
| Edge Functions | ✅ | ✅ |
| Build Minutes (Free) | 300/month | 6000/month |
| Bandwidth (Free) | 100GB/month | 100GB/month |

## Benefits of Migration

1. **Better Next.js Integration**: Vercel is the creator of Next.js, providing optimal performance and features
2. **Vercel Blob Storage**: Native file storage solution with better API integration
3. **Infrastructure as Code**: Terraform support for reproducible deployments
4. **Improved Build Performance**: Faster builds with better caching
5. **Enhanced Analytics**: Built-in Web Vitals and performance monitoring

## Cleanup Tasks

After confirming the Vercel deployment is working correctly, you can:

1. Remove old Netlify files:
   - `atlasfluvial-site/netlify.toml`
   - `atlasfluvial-site/deploy.py`
   - `src/pdf_generator/netlify_uploader.py`

2. Remove Netlify environment variables from `.env`

3. Update any CI/CD pipelines to use Vercel deployment

## Troubleshooting

### Common Issues

1. **Deployment fails with "Project not found"**
   - Ensure you've linked the project: `vercel link`

2. **Blob Storage upload fails**
   - Verify BLOB_READ_WRITE_TOKEN is set correctly
   - Check Blob Storage is enabled in Vercel dashboard

3. **Build errors**
   - Ensure Node.js version 18 is being used
   - Clear cache: `vercel --force`

### Support Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Blob Storage Guide](https://vercel.com/docs/storage/vercel-blob)
- [Terraform Vercel Provider](https://registry.terraform.io/providers/vercel/vercel/latest/docs)

## Next Steps

1. Test the deployment thoroughly
2. Update DNS records if using custom domain
3. Monitor performance and costs
4. Remove old Netlify resources after successful migration