# Monitoramento de Builds e Releases

Este projeto é um script em Python que monitora o status de builds no GitHub Actions e novas releases de um repositório, enviando notificações para um webhook configurado (ex.: Discord).

## Funcionalidades

- **Monitoramento de Builds:** Verifica continuamente o status das builds configuradas e notifica mudanças de estado (em progresso, na fila, concluída com sucesso, falha, etc.).
- **Monitoramento de Releases:** Monitora novas releases no repositório e notifica sobre mudanças na tag `latest`.
- **Notificações:** Envia notificações para um webhook configurado com as informações relevantes.

## Requisitos

- Python 3.7+
- Biblioteca `requests`
- Biblioteca `python-dotenv`

## Configuração

1. **Clonar o Repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd <nome-do-repositorio>
   ```

2. **Instalar Dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar Variáveis de Ambiente:**

   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

   ```env
   BUILD_API_URLS=["<URL_API_BUILD_1>", "<URL_API_BUILD_2>"]
   RELEASES_API_URL=<URL_API_RELEASES>
   NOTIFICATION_WEBHOOK=<URL_DO_WEBHOOK>
   ```

   - **BUILD_API_URLS:** Lista de URLs da API pública para as builds a serem monitoradas.
   - **RELEASES_API_URL:** URL da API pública das releases do repositório.
   - **NOTIFICATION_WEBHOOK:** URL do webhook para envio das notificações.

## Uso

Execute o script principal:

```bash
python monitor.py
```

O script:
- Monitora builds e releases a cada 10 minutos.
- Envia notificações para o webhook configurado com informações sobre mudanças no status das builds ou novas releases.

## Estrutura do Projeto

```
.
├── monitor.py      # Script principal
├── .env            # Arquivo de configuração com variáveis de ambiente
├── requirements.txt # Dependências do projeto
```

## Exemplos de Notificações

- **Build em progresso:**
  ```
  ⏳ Build 123456 está em execução.
  ```

- **Build concluída com sucesso:**
  ```
  ✅ Build 123456 concluída com sucesso!
  ```

- **Nova release:**
  ```
  🚀 Nova release disponível: **Versão 1.0.0**
  Tag: `v1.0.0`
  Veja mais: https://github.com/seu-repo/releases
  ```

## Contribuições

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature/bugfix:
   ```bash
   git checkout -b minha-feature
   ```
3. Envie seu PR para análise.

## Licença

Este projeto é licenciado sob a [MIT License](LICENSE).

