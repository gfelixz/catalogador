# MetaCritic Clone - Sistema de Agregação de Avaliações

Um software em Python inspirado no Metacritic que permite agregar avaliações de produtos (jogos, filmes, música, TV shows).

## Funcionalidades

- ✅ Cadastro de produtos (jogos, filmes, séries, músicas)
- ✅ Sistema de avaliações de críticos e usuários
- ✅ Cálculo automático do Metascore (média das avaliações de críticos)
- ✅ Cálculo da pontuação de usuários
- ✅ Interface web responsiva e moderna
- ✅ Sistema de cores baseado na pontuação (verde, amarelo, vermelho)
- ✅ Categorização por tipo de mídia
- ✅ Armazenamento em JSON (sem necessidade de banco de dados)

## Como Usar

### Instalação

1. Instale as dependências:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Executar a Aplicação

\`\`\`bash
python app.py
\`\`\`

Acesse: `http://localhost:5000`

## Estrutura do Projeto

- `app.py` - Aplicação Flask principal
- `templates/` - Templates HTML
- `data.json` - Arquivo de dados (gerado automaticamente)

## Como Funciona

### Adicionar Produtos
1. Clique em "Adicionar Produto"
2. Preencha o formulário com título, categoria, data de lançamento, etc
3. O produto será listado na página inicial

### Adicionar Avaliações
1. Acesse a página de detalhes do produto
2. Clique em "Adicionar Avaliação"
3. Escolha o tipo (crítico ou usuário)
4. Digite a pontuação (0-100)
5. Adicione um comentário (opcional)

### Sistema de Pontuação

**Metascore (Críticos):**
- 75-100: Verde (Excelente)
- 50-74: Amarelo (Mediano)
- 0-49: Vermelho (Ruim)

**User Score (Usuários):**
- Escala de 0-10
- Calculada como média de todas as avaliações de usuários

## Tecnologias

- Python 3
- Flask (Framework web)
- HTML/CSS (Interface)
- JSON (Armazenamento de dados)
