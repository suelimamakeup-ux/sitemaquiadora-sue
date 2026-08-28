---
name: Maquiadora Sue
description: Alta maquiagem e penteado para noivas, debutantes e grandes ocasiões no Rio de Janeiro
colors:
  primary: "#D4AF37"        # Gold accent - sofisticação e luxo
  onPrimary: "#FFFFFF"
  surface: "#FDFBF9"        # Fundo premium creme
  onSurface: "#1C1C1C"      # Texto escuro elegante
  muted: "#444444"          # Texto secundário
  danger: "#B3261E"
typography:
  display:
    fontFamily: Playfair Display
    fontSize: 2.25rem
    fontWeight: 400
    lineHeight: 1.2
    letterSpacing: 0.5px
  body:
    fontFamily: Lato
    fontSize: 1rem
    fontWeight: 300
    lineHeight: 1.8
  label:
    fontFamily: Lato
    fontSize: 0.875rem
    fontWeight: 600
rounded:
  sm: 4px
  md: 8px
  lg: 16px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 48px
components:
  button:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.onPrimary}"
    rounded: "{rounded.sm}"
    padding: "{spacing.sm} {spacing.md}"
  buttonSecondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.onSurface}"
    rounded: "{rounded.sm}"
    padding: "{spacing.sm} {spacing.md}"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.onSurface}"
    rounded: "{rounded.sm}"
    padding: "{spacing.lg}"
  caption:
    textColor: "{colors.muted}"
  alert:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.danger}"
    rounded: "{rounded.sm}"
    padding: "{spacing.md}"
---

## Overview
Sofisticação e exclusividade. Transmitir premium e confiança para noivas e debutantes que buscam o melhor dia das suas vidas. Visual limpo, elegante, sem exagero.

Quem usa: noivas, debutantes e mães de formandas. Usa no celular, com calma, planejando um evento especial. O sucesso é agendar uma consulta via WhatsApp.

## Colors
- **primary** - Gold #D4AF37. Cor da marca, usada em destaques, botões principais e ícones. Cor de sofisticação.
- **surface / onSurface** - Fundo creme #FDFBF9 e texto escuro #1C1C1C. Onde 90% da tela vive.
- **muted** - Texto secundário #444444, legendas, descrições. Nunca para texto principal.
- **danger** - Só para erros e ações destrutivas. Nunca decorativo.

Sem gradiente. Uma cor de destaque só (gold).

## Typography
Duas famílias: Playfair Display para títulos (display), Lato para corpo e labels.
Hierarquia por tamanho e peso, não por cor nova.

## Layout
Grade de 8px - todo espaçamento é múltiplo de 8. Largura máxima de texto: 72 caracteres.
Espaço em branco é a decoração. Respiro generoso entre seções.

## Elevation & Depth
Padrão: sem sombra. Separação por borda de 1px em #EFEBE4.
Sombra só no botão flutuante do WhatsApp (elemento que realmente flutua).

## Shapes
rounded.sm (4px) em botões e cards. Nada com raio maior que 16px.
Avatar do perfil: círculo (50% border-radius).

## Components
- **button** - Ação principal: "Iniciar Atendimento", "Conversar no WhatsApp", "Solicitar Orçamento". Sempre no infinitivo.
- **buttonSecondary** - "Conhecer Pacotes", "Ver Opções". Contorno ou texto.
- **card** - Um assunto por card. Bordas leves, fundo claro.
- **caption** - Legenda e texto de apoio. Sempre em muted.

## Do's and Don'ts
**Não faça:**
1. Gradiente roxo/azul. Use gold chapado.
2. Sombra em tudo. Só no WhatsApp float.
3. Emoji como ícone. Use FontAwesome.

**Faça:**
1. Uma ação primária por seção (WhatsApp).
2. Todo espaçamento múltiplo de 8.
3. Texto escuro sobre fundo creme - se precisou de cor nova, o problema é hierarquia.
4. Manter consistência entre biosite e site institucional.
