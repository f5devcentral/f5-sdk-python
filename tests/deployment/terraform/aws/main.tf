module "utils" {
  source = "../utils"
}

provider "aws" {
  region = "${var.aws_region}"
}

# Create 'supporting' network infrastructure for the BIG-IP VMs
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = "aws-vpc-${module.utils.env_prefix}"
  }
}
resource "aws_internet_gateway" "gateway" {
  vpc_id = "${aws_vpc.main.id}"
  tags = {
    Name = "aws-internet-gateway-${module.utils.env_prefix}"
  }
}
resource "aws_route_table" "mgmt" {
  vpc_id = "${aws_vpc.main.id}"
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.gateway.id}"
  }
  tags = {
    Name = "aws-route-table-mgmt-${module.utils.env_prefix}"
  }
}

resource "aws_route_table" "external" {
  vpc_id = "${aws_vpc.main.id}"
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.gateway.id}"
  }
  tags = {
    Name = "aws-route-table-external-${module.utils.env_prefix}"
  }
}

resource "aws_subnet" "mgmtAz1" {
  vpc_id = "${aws_vpc.main.id}"
  availability_zone = "${var.aws_region}a"
  cidr_block = "10.0.0.0/24"
  tags = {
    Name = "aws-subnet-mgmtAz1-${module.utils.env_prefix}"
  }
}

resource "aws_route_table_association" "mgmtAz1" {
  subnet_id      = "${aws_subnet.mgmtAz1.id}"
  route_table_id = "${aws_route_table.mgmt.id}"
}

resource "aws_subnet" "externalAz1" {
  vpc_id = "${aws_vpc.main.id}"
  availability_zone = "${var.aws_region}a"
  cidr_block = "10.0.1.0/24"
  tags = {
    Name = "aws-subnet-externalAz1-${module.utils.env_prefix}"
  }
}

resource "aws_route_table_association" "externalAz1" {
  subnet_id      = "${aws_subnet.externalAz1.id}"
  route_table_id = "${aws_route_table.external.id}"
}

# Creates a BIG-IP for testing
resource "aws_security_group" "external" {
  description = "External interface rules"
  vpc_id = "${aws_vpc.main.id}"
  ingress {
    from_port = 80
    to_port = 80
    protocol = 6
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 443
    to_port = 443
    protocol = 6
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 4353
    to_port = 4353
    protocol = 6
    self = true
  }
  ingress {
    from_port = 1026
    to_port = 1026
    protocol = 17
    self = true
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "aws-security-group-external-${module.utils.env_prefix}"
  }
}

resource "aws_security_group" "mgmt" {
  description = "External interface rules"
  vpc_id = "${aws_vpc.main.id}"
  ingress {
    from_port = 22
    to_port = 22
    protocol = 6
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 443
    to_port = 443
    protocol = 6
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 443
    to_port = 443
    protocol = 6
    security_groups = ["${aws_security_group.external.id}"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "aws-security-group-mgmt-${module.utils.env_prefix}"
  }
}

resource "aws_s3_bucket" "configdb" {
  bucket = "aws-s3-bucket-${module.utils.env_prefix}"
  force_destroy = true
  tags = {
    Name = "aws-s3-bucket-${module.utils.env_prefix}"
  }
}

resource "aws_iam_role" "main" {
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
  tags = {
     Name = "aws-iam-role-${module.utils.env_prefix}"
  }
}

resource "aws_iam_role_policy" "BigIpPolicy" {
  name = "aws-iam-role-policy-${module.utils.env_prefix}"
  role = "${aws_iam_role.main.id}"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
        "Action": [
            "ec2:DescribeInstances",
            "ec2:DescribeInstanceStatus",
            "ec2:DescribeAddresses",
            "ec2:AssociateAddress",
            "ec2:DisassociateAddress",
            "ec2:DescribeNetworkInterfaces",
            "ec2:DescribeNetworkInterfaceAttribute",
            "ec2:DescribeRouteTables",
            "ec2:ReplaceRoute",
            "ec2:CreateRoute",
            "ec2:assignprivateipaddresses",
            "sts:AssumeRole",
            "s3:ListAllMyBuckets"
        ],
        "Resource": [
            "*"
        ],
        "Effect": "Allow"
    },
    {
        "Action": [
            "s3:ListBucket",
            "s3:GetBucketTagging"
        ],
        "Resource": "arn:aws:s3:::${aws_s3_bucket.configdb.id}",
        "Effect": "Allow"
    },
    {
        "Action": [
            "s3:PutObject",
            "s3:GetObject",
            "s3:DeleteObject"
        ],
        "Resource": "arn:aws:s3:::${aws_s3_bucket.configdb.id}/*",
        "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_instance_profile" "instance_profile" {
  name = "aws-iam-instance-profile-${module.utils.env_prefix}"
  role = "${aws_iam_role.main.id}"
}

resource "aws_network_interface" "mgmt1" {
  subnet_id = "${aws_subnet.mgmtAz1.id}"
  security_groups = ["${aws_security_group.mgmt.id}"]
  description = "Management Interface for BIG-IP"
  tags = {
    Name = "aws-network-interface-mgmt1-${module.utils.env_prefix}"
  }
}

resource "aws_eip" "mgmt1" {
  vpc = true
  network_interface = "${aws_network_interface.mgmt1.id}"
  associate_with_private_ip = "${tolist(aws_network_interface.mgmt1.private_ips)[0]}"
  tags = {
    Name = "aws-eip-mgmt1-${module.utils.env_prefix}"
  }
}

resource "aws_network_interface" "external1" {
  subnet_id = "${aws_subnet.externalAz1.id}"
  security_groups = ["${aws_security_group.external.id}"]
  description = "Public External Interface for the BIG-IP"
  private_ips_count = 1
  tags = {
    Name = "aws-network-interface-external1-${module.utils.env_prefix}"
  }
}

resource "aws_eip" "external1" {
  vpc = true
  network_interface = "${aws_network_interface.external1.id}"
  associate_with_private_ip = "${tolist(aws_network_interface.external1.private_ips)[0]}"
  tags = {
    Name = "aws-eip-external1-${module.utils.env_prefix}"
  }
}

data "template_file" "user_data_vm0" {
  template = "${file("${path.module}/user_data.tpl")}"
  vars = {
    admin_username  = "${var.admin_username}"
    admin_password  = "${module.utils.admin_password}"
    external_self   = "${aws_network_interface.external1.private_ip}/24"
  }
}

resource "null_resource" "delay" {
  provisioner "local-exec" {
    command = "sleep 30"
  }
}

resource "aws_instance" "vm0" {
  ami = "${var.aws_bigip_ami_id}"
  instance_type = "m5.xlarge"
  availability_zone = "${var.aws_region}a"
  key_name = "dewpt"
  network_interface {
    network_interface_id = "${aws_network_interface.mgmt1.id}"
    device_index = 0
  }
  network_interface {
    network_interface_id = "${aws_network_interface.external1.id}"
    device_index = 1
  }
  iam_instance_profile = "${aws_iam_instance_profile.instance_profile.name}"
  user_data = "${data.template_file.user_data_vm0.rendered}"
  tags = {
     Name = "sdkbigip-vm0-${module.utils.env_prefix}"
  }
  # Wait until the instance is in a running state
  provisioner "local-exec" {
    command = "aws ec2 wait instance-status-ok --instance-ids ${aws_instance.vm0.id} --region ${var.aws_region}"
  }
  depends_on = [null_resource.delay]
}

resource "local_file" "do0" {
    content = "${templatefile(
      "${path.module}/../../declarations/do/aws_do_template.json",
      {
        hostname = "sdkbigipvm0.local",
        admin_username = "${var.admin_username}",
        admin_password = "${module.utils.admin_password}",
        external_self = "${aws_network_interface.external1.private_ip}",
        remote_host = "${aws_network_interface.mgmt1.private_ip}"
      }
    )}"
    filename = "${path.module}/temp_do0.json"
}

resource "null_resource" "login0" {
  provisioner "local-exec" {
    command = "f5 bigip configure-auth --host ${aws_eip.mgmt1.public_ip} --user ${var.admin_username} --password ${module.utils.admin_password}"
  }
  triggers = {
    always_run = fileexists("${path.module}/../../declarations/do/aws_do_template.json")
  }
  depends_on = [aws_instance.vm0]
}

resource "null_resource" "onboard0" {
  provisioner "local-exec" {
    command = "f5 bigip toolchain service create --install-component --component do --declaration ${path.module}/temp_do0.json"
  }
  triggers = {
    always_run = fileexists("${path.module}/../../declarations/do/aws_do_template.json")
  }
  depends_on = [local_file.do0, null_resource.login0]
}

output "deployment_info" {
  value = {
    instances: [
      {
        admin_username = var.admin_username,
        admin_password = module.utils.admin_password,
        mgmt_address = aws_eip.mgmt1.public_ip,
        instanceId = aws_instance.vm0.id,
        mgmt_port = 443,
        primary = false
      },
    ],
    deploymentId: module.utils.env_prefix,
    environment: "aws",
    region: var.aws_region
  }
}
