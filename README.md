# Teste de conexão do Gestor no Vercel

Este projeto serve apenas para verificar se uma função Python hospedada no
Vercel consegue alcançar o SQL Server do Gestor.

Ele não possui consultas de estoque, notas fiscais ou envio de e-mail.

## Arquivos

- `app.py`: API FastAPI com a rota de teste.
- `requirements.txt`: dependências instaladas pelo Vercel.

## Configuração

Os dados de conexão estão diretamente no `app.py`. Para este teste temporário,
não é necessário cadastrar variáveis de ambiente no Vercel.

## Testes

Abra primeiro:

```text
https://SEU-PROJETO.vercel.app/
```

O retorno esperado é:

```json
{
  "status": "ok",
  "mensagem": "API de teste do Gestor iniciada.",
  "proximo_teste": "/teste-gestor"
}
```

Depois abra:

```text
https://SEU-PROJETO.vercel.app/teste-gestor
```

Quando o banco estiver acessível, o retorno terá:

```json
{
  "status": "ok",
  "mensagem": "Vercel conectou ao Gestor com sucesso."
}
```

Se aparecer `status: erro`, copie o conteúdo de `tipo` e `detalhe`. Esses
campos permitem diferenciar falha de rede, porta, autenticação, banco ou
protocolo SQL Server.

## Como publicar

Crie um repositório contendo estes arquivos e importe-o no Vercel, ou use a
CLI do Vercel dentro desta pasta. O arquivo `app.py` é um ponto de entrada
FastAPI reconhecido pelo runtime Python.
