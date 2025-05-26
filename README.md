# Utilização de Técnicas de Machine Learning para predizer campos que são obrigatórios o preenchimento no Sales Force

## Exeplicação do mini Projeto

- Na criação de casos no Sales Force é obrigatório o preenchimento dos seguintes campos: Corpo(Feed), Produto relacionado, Motivo do contato, Ação necessária, Diagnóstico do problema
- O software serve para, no momento em que você copia o relatório criado pelo analista no Feed e cola em um determinado campo do programa, os campos Produto relacionado, Motivo do contato, Ação necessária e Diagnóstico do problema são sugeridos ao clicar em Analisar

### Artefato 1
- Utilização da técnica Randon Forest
- Questões a serem abordadas:
  - Precisamos mapear todos os setores que utilizam a ferramenta
  - Depois, mapear todos os produtos que são prestado suporte
  - E então, utilizar uma quantidade de registros considerável para treinar a predição dos campos do Sales Force
- No momento, com 10k foi realizado um protótipo funcional que o pré-processamento não leva em consideração os fatores acima, sendo possível entender que o dataset está desbalanceado desse primeiro artefato.

### Artefato 2
- Utilização de Redes Neurais
