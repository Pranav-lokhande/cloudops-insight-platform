variable "aws_region" { type = string, default = "eu-north-1" }
variable "ami_id" { description = "Valid Ubuntu AMI ID for the selected region", type = string }
variable "instance_type" { type = string, default = "t3.micro" }
variable "key_name" { description = "Existing EC2 key pair name", type = string }
variable "admin_cidr" { description = "Your public IP in CIDR notation, e.g. x.x.x.x/32", type = string }
