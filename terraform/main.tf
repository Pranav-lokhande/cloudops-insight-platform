data "aws_vpc" "default" { default = true }
data "aws_subnets" "default" {
  filter { name = "vpc-id", values = [data.aws_vpc.default.id] }
}
resource "aws_security_group" "cloudops" {
  name = "cloudops-insight-sg"
  description = "Learning project HTTP and restricted SSH"
  vpc_id = data.aws_vpc.default.id
  ingress {
    description = "HTTP web application"
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "SSH from administrator IP only"
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = [var.admin_cidr]
  }
  egress { from_port = 0, to_port = 0, protocol = "-1", cidr_blocks = ["0.0.0.0/0"] }
  tags = { Name = "cloudops-insight-sg", Project = "CloudOpsInsight" }
}
resource "aws_instance" "cloudops" {
  ami = var.ami_id
  instance_type = var.instance_type
  key_name = var.key_name
  subnet_id = data.aws_subnets.default.ids[0]
  vpc_security_group_ids = [aws_security_group.cloudops.id]
  associate_public_ip_address = true
  root_block_device { volume_size = 12, volume_type = "gp3", encrypted = true }
  tags = { Name = "cloudops-insight", Project = "CloudOpsInsight" }
}
