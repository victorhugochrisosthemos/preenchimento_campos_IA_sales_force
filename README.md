# Utilização de Técnicas de Machine Learning para predizer campos que são obrigatórios o preenchimento no Sales Force

## Explicação do Projeto

- Na criação de casos no Sales Force é obrigatório o preenchimento dos seguintes campos: Corpo(Feed), Produto relacionado, Motivo do contato, Ação necessária, Diagnóstico do problema
- O software serve para, no momento em que você copia o relatório criado pelo analista no Feed e cola em um determinado campo do programa, os campos Produto relacionado, Motivo do contato, Ação necessária e Diagnóstico do problema são sugeridos ao clicar em Analisar
- Quando o Motivo do Caso é 'Situação alegado pelo cliente', necessariamente precisa preencher o campo Diagnóstico

### Artefato 1

![Screenshot_1](https://github.com/user-attachments/assets/9001b919-689a-4f41-a0af-2035cce6c9d3)


- Utilização da técnica Randon Forest
- Questões a serem abordadas:
  - Precisamos mapear todos os setores que utilizam a ferramenta
  - Depois, mapear todos os produtos que são prestado suporte
  - E então, utilizar uma quantidade de registros considerável para treinar a predição dos campos do Sales Force
- No momento, com 10k foi realizado um protótipo funcional que o pré-processamento não leva em consideração os fatores acima, sendo possível entender que o dataset está desbalanceado desse primeiro artefato.
- Sobre os registros considerados, foi selecionado analista que demonstram um boa frequência de preenchimento correto dos dados no Sales Force
- Precisa realizar testes para definir a acurácia
- Foi gerado um executável a fim de demonstrar os resultados a equipes da Intelbras

### Artefato 2

![image](https://github.com/user-attachments/assets/e6416342-d456-4400-949d-86c5d42ecb48)


- Utilização de Redes Neurais
- Problemas relacionados à processamento de dados ainda persiste, precisamos organizar os dados
