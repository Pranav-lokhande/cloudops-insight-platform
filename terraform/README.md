# Terraform starter
Provisions one EC2 instance and a security group; it does not install Docker or the app yet.
Copy `terraform.tfvars.example` to `terraform.tfvars`, fill valid region-specific AMI, key pair and your public IP CIDR. Configure AWS credentials through a profile or environment, never hard-code access keys. Run `terraform init`, `terraform fmt`, `terraform validate`, `terraform plan`, review carefully, then `terraform apply`. Destroy the lab when finished. This starter uses local state; S3 remote state is a later step.
