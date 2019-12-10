

variable "aws_region" {
  description = "The AWS Region in which the resources in this example should exist"
  default     = "us-west-2"
}

variable "aws_bigip_ami_id" {
  default = "ami-031ffd3d4362f7a94"
}

variable "offer" {
  default = "f5-big-ip-good"
}

variable "sku" {
  default = "f5-bigip-virtual-edition-25m-good-hourly"
}

variable "bigip_version" {
  description = "The BIG-IP version for the virtual machine"
  default     = "latest"
}

variable "instance_size" {
  description = "The instance size for the virtual machine"
  default     = "Standard_DS3_v2"
}

variable "admin_username" {
  description = "The admin username for the virtual machine"
  default     = "awsuser"
}
