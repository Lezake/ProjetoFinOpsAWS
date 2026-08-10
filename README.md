# ☁️ AWS FinOps Automation: Cost Optimization for Non-Production Environments

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## 📌 Visão Geral do Projeto

Este projeto implementa uma arquitetura automatizada de **FinOps (Cloud Cost Optimization)** na AWS. O objetivo principal é reduzir os custos operacionais desligando sistemicamente ambientes de Desenvolvimento fora do horário comercial (Sexta 20h às Segunda 08h), enquanto garante, através de um forte isolamento de tags e permissões, que o ambiente de Produção permaneça intacto operando 24/7.

Além do desligamento de instâncias (EC2/ASG) e bancos de dados (RDS), a automação atua na limpeza de volumes EBS órfãos, evitando cobranças residuais indesejadas.

## 📐 Arquitetura

> **[INSERIR IMAGEM AQUI]**
> *(Adicione o arquivo `docs/architecture.png` mostrando o fluxo: EventBridge -> Lambda -> ASG/RDS/EBS)*

## 🚀 Principais Features e Decisões Técnicas

*   **Infraestrutura como Código (IaC):** Todo o ambiente (Dev e Prod) foi provisionado via **Terraform**, garantindo reprodutibilidade e controle de versão.
*   **Estratégia Estrita de Tagging:** A lógica de automação não depende de IDs fixos, mas sim de tags dinâmicas (`environment=dev` vs `environment=prod`). Isso protege o ambiente de Produção contra falhas humanas (Blast Radius contido).
*   **Segurança (Least Privilege):** Implementação de políticas IAM granulares:
    *   *Role A (Stop/Cleanup):* Permissão apenas para ler recursos, zerar ASGs, pausar RDS e deletar discos `available`.
    *   *Role B (Start):* Permissão apenas para ler recursos, restaurar ASGs e iniciar RDS.
*   **Automação Serverless:** Funções **AWS Lambda** escritas em **Python (Boto3)** para execução rápida e sem custo de servidores ociosos.
*   **Event-Driven Scheduling:** Agendamento via **Amazon EventBridge (Cron)** configurado para respeitar os fusos horários locais da operação.

## 🛠️ Stack Tecnológica

*   **Cloud Provider:** AWS
*   **Compute & Database:** Amazon EC2, Auto Scaling Groups (ASG), Amazon RDS
*   **Serverless & Automação:** AWS Lambda, Amazon EventBridge, AWS IAM
*   **IaC:** Terraform
*   **Linguagem:** Python (Boto3)

## 📂 Estrutura do Repositório

- `/terraform`: Configurações de Infraestrutura como Código (Módulos e Ambientes).
- `/src`: Scripts Python contendo a lógica do Boto3 para as funções Lambda.
- `/docs`: Documentação adicional e diagramas de arquitetura.