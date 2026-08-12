terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-2"
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}

resource "aws_launch_template" "padrao_micro" {
  name_prefix   = "modelo-base-"
  image_id      = data.aws_ami.amazon_linux.id
  instance_type = "t2.micro"
}

resource "aws_autoscaling_group" "asg_dev_frontend" {
  name               = "asg-dev-frontend"
  availability_zones = ["us-east-2a", "us-east-2b"]
  desired_capacity   = 1
  max_size           = 1
  min_size           = 0

  launch_template {
    id      = aws_launch_template.padrao_micro.id
    version = "$Latest"
  }

  tag {
    key                 = "ambiente"
    value               = "dev"
    propagate_at_launch = true
  }
  tag {
    key                 = "Name"
    value               = "dev-frontend-asg"
    propagate_at_launch = true
  }
}

resource "aws_autoscaling_group" "asg_dev_backend" {
  name               = "asg-dev-backend"
  availability_zones = ["us-east-2a", "us-east-2b"]
  desired_capacity   = 1
  max_size           = 1
  min_size           = 0

  launch_template {
    id      = aws_launch_template.padrao_micro.id
    version = "$Latest"
  }

  tag {
    key                 = "ambiente"
    value               = "dev"
    propagate_at_launch = true
  }
  tag {
    key                 = "Name"
    value               = "dev-backend-asg"
    propagate_at_launch = true
  }
}

resource "aws_autoscaling_group" "asg_prod" {
  name               = "asg-prod"
  availability_zones = ["us-east-2a", "us-east-2b"]
  desired_capacity   = 1
  max_size           = 1
  min_size           = 0

  launch_template {
    id      = aws_launch_template.padrao_micro.id
    version = "$Latest"
  }

  tag {
    key                 = "ambiente"
    value               = "prod"
    propagate_at_launch = true
  }
  tag {
    key                 = "Name"
    value               = "prod-asg"
    propagate_at_launch = true
  }
}

resource "aws_db_instance" "banco_dev" {
  identifier          = "banco-dev"
  allocated_storage   = 20
  storage_type        = "gp2"
  engine              = "mysql"
  engine_version      = "8.0"
  instance_class      = "db.t3.micro"
  username            = var.db_username
  password            = var.db_password
  skip_final_snapshot = true

  tags = {
    Name     = "banco-dev"
    ambiente = "dev"
  }
}

resource "aws_db_instance" "banco_prod" {
  identifier          = "banco-prod"
  allocated_storage   = 20
  storage_type        = "gp2"
  engine              = "mysql"
  engine_version      = "8.0"
  instance_class      = "db.t3.micro"
  username            = var.db_username
  password            = var.db_password
  skip_final_snapshot = true

  tags = {
    Name     = "banco-prod"
    ambiente = "prod"
  }
}