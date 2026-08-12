variable "db_username" {
  description = "Usuário do banco de dados RDS"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Senha do banco de dados RDS"
  type        = string
  sensitive   = true
}