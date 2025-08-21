# Personal-Finance-Analysis



# 1. Descrição

Este projeto tem como objetivo a análise exploratória, modelagem de risco e segmentação de perfis financeiros a partir de um dataset sintético de finanças pessoais contendo mais de 32 mil registros individuais. O conjunto de dados representa comportamentos realistas de renda, despesas, poupança, empréstimos e crédito, abrangendo diferentes regiões, faixas etárias, profissões e níveis educacionais.

A análise desenvolvida incluiu desde o pré-processamento dos dados, passando por avaliações univariadas, bivariadas e multivariadas, até a construção de modelos de segmentação de risco, utilizando tanto regras de negócio quanto abordagens estatísticas, como o Gaussian Mixture Model (GMM).

O estudo permitiu identificar fatores críticos que influenciam o credit score e o risco de inadimplência, como renda mensal, proporção dívida/renda, nível educacional, estabilidade profissional e reservas financeiras. Além disso, foram criados grupos estratégicos de perfis de risco, úteis para aplicações em previsão de crédito, análise de risco e segmentação de clientes.

# 2. Tecnologias e Ferramentas
O projeto foi desenvolvido em Python e fez uso de diversas bibliotecas do ecossistema de Ciência de Dados e Machine Learning:

- Pandas: para manipulação, limpeza e transformação dos dados.
- NumPy: para cálculos numéricos e operações vetorizadas.
- Matplotlib e Seaborn: para a criação de visualizações estatísticas e gráficos analíticos.
- SciPy: para aplicação de testes estatísticos, como o qui-quadrado.
- Scikit-learn: para a modelagem estatística, incluindo o uso de Gaussian Mixture Models (GMM) na identificação de padrões naturais.
- KaggleHub: para integração e acesso ao dataset diretamente a partir do repositório no Kaggle.

Essa combinação de ferramentas possibilitou um fluxo completo de exploração de dados, visualização, análise estatística e modelagem preditiva, garantindo robustez e flexibilidade na análise.

# 3.Problema de negocio e o objetivo do projeto

Instituições financeiras, fintechs e bancos enfrentam o desafio de avaliar corretamente o risco de crédito dos clientes. Um processo ineficiente pode gerar dois problemas graves:

- Conceder crédito a clientes de alto risco, aumentando a inadimplência.

- Recusar crédito a clientes de baixo risco, perdendo oportunidades de negócios rentáveis.

Além disso, fatores como renda, nível educacional, estabilidade no emprego, proporção dívida/renda e hábitos de poupança influenciam diretamente a capacidade de pagamento de um indivíduo. Assim, surge a necessidade de modelos robustos que combinem variáveis financeiras, demográficas e comportamentais para prever risco de forma mais precisa.

O objetivo do projeto é desenvolver uma análise exploratória e modelos de segmentação de risco de crédito utilizando dados financeiros individuais. Em especial, busca-se:

- Identificar as variáveis mais relevantes que impactam a pontuação de crédito (credit score).
- Construir perfis de risco a partir de métricas como debt-to-income ratio e savings-to-income ratio.
- Implementar diferentes abordagens de segmentação de risco (percentis e Gaussian Mixture Models).
- Criar grupos estratégicos de clientes (Premium, Standard, Basic), auxiliando na tomada de decisão sobre concessão de crédito.
- Fornecer insights para estratégias de negócio, reduzindo inadimplência e melhorando a alocação de crédito.

## 4.Comparação das Abordagens de Modelagem de Risco de Crédito

A modelagem de risco de crédito apresentada foi desenvolvida em duas abordagens distintas, cada uma com características complementares.  

A primeira, denominada **Risk Analysis**, segue um caminho orientado por regras de negócio e fundamentação estatística. Nela, foram estabelecidos índices compostos, como o *Financial Stability Index*, e aplicados limiares percentílicos de risco (baixo, médio e alto) complementados por regras de reclassificação. Esse método permitiu construir perfis hierárquicos de crédito (Premium Elite, Standard Secure, Basic Vulnerable, entre outros), traduzindo diretamente os resultados em categorias compreensíveis e aplicáveis no mercado financeiro. Essa abordagem apresenta maior interpretabilidade e está mais alinhada às práticas de análise de crédito, embora dependa fortemente de suposições iniciais do analista.  

A segunda abordagem, denominada **Unsupervised Analysis**, adota uma estratégia totalmente orientada pelos dados, com técnicas de clusterização não supervisionada (KMeans, MiniBatchKMeans e Hierárquico), seleção do número ótimo de grupos via *silhouette score* e redução de dimensionalidade por PCA para melhor interpretação visual. Além disso, incorpora tratamento robusto de outliers e pré-processamento padronizado. Essa metodologia se destaca pela capacidade de revelar padrões ocultos e subgrupos dentro da base, sem imposição de regras rígidas, sendo ideal para exploração inicial e descobertas inesperadas. Contudo, a interpretação dos clusters exige uma etapa posterior de tradução em critérios de risco, uma vez que os grupos encontrados não necessariamente se alinham de forma imediata às práticas regulatórias.  

Dessa forma, a escolha da melhor abordagem depende do objetivo. Se a prioridade é entregar perfis de crédito prontos, claros e justificáveis para aplicação prática, a **Risk Analysis** é a mais adequada. Já se a meta é explorar padrões emergentes, testar granularidades diferentes e identificar nuances do comportamento financeiro dos clientes, a **Unsupervised Analysis** agrega maior valor. Idealmente, ambas podem ser usadas de forma complementar: a análise não supervisionada para exploração inicial e a análise baseada em regras para estruturação final dos perfis.  

---

### 📊 Tabela Comparativa

| Critério                         | Risk Analysis (Regras + Estatística) | Unsupervised Analysis (Clusterização) |
|----------------------------------|---------------------------------------|----------------------------------------|
| **Abordagem**                   | Supervisionada / Regras de negócio    | Não supervisionada / Data-driven       |
| **Metodologia principal**       | Índice de estabilidade + GMM + regras de reclassificação | KMeans, MiniBatchKMeans, Clusterização hierárquica, PCA |
| **Interpretação**               | Direta, com perfis hierárquicos claros (Premium, Standard, Basic) | Indireta, exige tradução dos clusters em perfis de risco |
| **Alinhamento regulatório**     | Alto – mais próximo da prática de crédito | Médio – necessita validação posterior |
| **Descoberta de padrões ocultos** | Limitada (regras pré-definidas)       | Forte – descoberta natural dos clusters |
| **Tratamento de outliers**      | Regras de truncamento e ajustes regionais/profissionais | Winsorize/remoção com estratégias configuráveis |
| **Aplicabilidade imediata**     | Alta – perfis prontos para uso        | Média – necessita interpretação adicional |
| **Exploração de granularidades** | Moderada – focada em faixas de risco  | Ampla – permite múltiplos níveis de clusterização |
| **Principal vantagem**          | Perfis de crédito claros e aplicáveis | Revelação de subgrupos e padrões ocultos |
| **Principal limitação**         | Dependência de regras pré-definidas   | Menor interpretabilidade inicial        |


# 5. Execute este projeto em sua máquina local
Pré-requisitos:

Antes de começar, certifique-se de ter o seguinte instalado em sua máquina:
- Python 3.11.4
- pip (Python package manager)
- Git (Version control tool)
- Kaggle(Credentials)

Depois de instalar, abra um terminal na sua máquina local e execute os seguintes comandos:

1. Clone o repositório:
<pre>
git clone https://github.com/Rob-CordJr/Personal-Finance-Analysis.git
</pre>

2. Navegue até o diretório do repositório clonado:
<pre>
cd Personal-Finance-Analysis
</pre>

3. Crie um ambiente virtual:
<pre>
python -m venv venv
</pre>

4. Ative o Ambiente Virtual:

Ative o ambiente virtual usado para isolar as dependências do projeto.

<pre>
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
</pre>

5. Instale suas dependencias e faça o download do dataset, executando o comando abaixo:

<pre>
python setup_data.py
</pre>

# 7. Modelo de Regressão Logistica

O modelo de **Regressão Logística** apresentou um desempenho satisfatório para a tarefa de previsão de risco de crédito, alcançando uma **AUC de 0,811**, o que indica uma boa capacidade de discriminar clientes entre **alto risco** e **baixo risco**. Além disso, o **Brier Score de 0,175** reforça a boa calibração das probabilidades, mostrando que as estimativas do modelo estão próximas da realidade observada.

Do ponto de vista de negócio, a matriz de confusão demonstra que o modelo identifica corretamente **4.128 clientes de alto risco**, enquanto classifica adequadamente **3.197 clientes de baixo risco**. Embora existam **1.437 falsos negativos** (clientes de alto risco classificados como baixo risco), o impacto desse erro pode ser mitigado ao ajustar o ponto de corte, conforme indicado pelo **KS Statistic de 0,510** e o melhor **cut-off em 0,537**. Isso oferece flexibilidade para priorizar a redução de inadimplência (diminuindo falsos negativos) ou ampliar o acesso ao crédito (diminuindo falsos positivos), de acordo com a estratégia da instituição financeira.

Outro ponto relevante é a análise da importância das variáveis, que mostra que o **índice de poupança em relação à renda (savings-to-income ratio)** é o fator mais determinante no risco de crédito, seguido pela **renda mensal** e pela **situação de emprego**. Isso indica que clientes com maior capacidade de poupança e estabilidade financeira tendem a apresentar menor risco, enquanto aqueles com baixa reserva ou vínculos profissionais frágeis possuem maior probabilidade de inadimplência.

Na prática, o modelo pode ser utilizado para **segmentação de clientes**, atribuindo perfis como **Baixo Risco**, **Médio Risco** e **Alto Risco**. Essa categorização permite decisões mais estratégicas, como:

* **Baixo Risco**: oferecer crédito com taxas mais atrativas, fortalecendo o relacionamento com o cliente.
* **Médio Risco**: aplicar políticas de monitoramento mais próximas e limites de crédito ajustados.
* **Alto Risco**: adotar medidas restritivas, como solicitação de garantias adicionais ou recusa de crédito.


# 8. Dataset link
The dataset was collected from kaggle.

Link: https://www.kaggle.com/datasets/miadul/personal-finance-ml-dataset

# 9. Contact me
Linkedin: https://www.linkedin.com/in/roberto-cordeiro-5749931a0/

Github: https://github.com/Rob-CordJr

Gmail: robertodossantos747@gmail.com
