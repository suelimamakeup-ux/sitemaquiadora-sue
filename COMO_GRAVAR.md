# Como Gravar o Vídeo de Apresentação

## Pré-requisitos
1. Instale o Playwright: `npx playwright install chromium`
2. Instale o OBS Studio (grátis): https://obsproject.com

## Passo a Passo

### 1. Prepare o OBS Studio
- Abra o OBS Studio
- Adicione uma nova cena: "Maquiadora Sue"
- Adicione uma fonte: **Captura de Janela** → selecione o navegador Chrome/Edge
- Configuração de gravação:
  - Resolução: 1920x1080
  - FPS: 30
  - Formato: MP4

### 2. Execute o Script Playwright
```bash
cd "C:\Users\Thaió\OneDrive\Documentos\Biosite e site Maquiadora Sue"
node record_site.js
```

### 3. Inicie a Gravação no OBS
- Clique em **Iniciar Gravação** no OBS
- O script vai mostrar todas as seções automaticamente
- Ao final, clique em **Parar Gravação**

### 4. Edite o Vídeo (Opcional)
- Adicione música de fundo suave
- Adicione narração (opcional)
- Exporte em 1080p

## Cenas do Vídeo (1:20 - 1:40)

| Tempo | Cena | O que aparece |
|-------|------|---------------|
| 0:00-0:06 | Hero | Página carrega, botão "Iniciar Atendimento" |
| 0:06-0:14 | Navegação | Menu desktop, responsivo |
| 0:14-0:22 | A Profissional | Foto da Sue, credenciais |
| 0:22-0:32 | A Experiência | 3 cards do processo |
| 0:32-0:42 | Especialidades | Noivas, Debutantes, Social |
| 0:42-0:55 | Portfólio | Galeria + Lightbox |
| 0:55-1:05 | Depoimentos | 3 cards de clientes |
| 1:05-1:12 | CTA Final | Botão WhatsApp |
| 1:12-1:18 | Footer | Contatos e redes sociais |
| 1:18-1:25 | Mobile | Menu hambúrguer |

## Dicas
- Grave em modo incógnito para evitar extensões
- Zoom do navegador em 100%
- Desative notificações do sistema
- Teste antes de gravar
