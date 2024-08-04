# CNN-ALZHEIMER-CLASSIFICATION
<a href="https://github.com/RicardoMourao-py/CNN-ALZHEIMER-CLASSIFICATION/actions/workflows/backend.yaml" target="_blank"><img src="https://github.com/RicardoMourao-py/CNN-ALZHEIMER-CLASSIFICATION/actions/workflows/backend.yaml/badge.svg" alt="Test"></a>
<a href="https://github.com/RicardoMourao-py/CNN-ALZHEIMER-CLASSIFICATION/actions/workflows/frontend.yaml" target="_blank"><img src="https://github.com/RicardoMourao-py/CNN-ALZHEIMER-CLASSIFICATION/actions/workflows/frontend.yaml/badge.svg" alt="Test"></a>

Classificação de imagens médicas de Alzheimer utilizando redes neurais convolucionais para a identificação da doença.

## Arquitetura

![image](https://github.com/user-attachments/assets/a1e166c2-6b3b-4738-bad1-6d9af590b934)

:one: O usuário faz o upload de uma imagem **png/jpeg** na submissão web, na qual é possível visualizar o **eixo axial** do cérebro via ressonância magnética. <br><br>
:two: Nesta etapa, a mesma imagem é armazenada em um bucket do Cloud Storage, em que funciona como **gatilho** para a etapa 3. <br><br>
:three: A Cloud Function é responsável por executar as próximas etapas via código, na qual ela é disparada **todas as vezes** em que o bucket do Cloud Storage recebe uma imagem. <br><br>
:four: O Vertex AI possui uma vasta quantidade de ferramentas para treinamento de modelos, *datasets* classificados e *endpoints* de modelos. Com isso, foi criado um *endpoint* que é chamado via código da Cloud Function para realizar a **previsão** da imagem armazenada no Cloud Storage. <br><br>
:five: Por fim, o resultado é retornado em um json e enviado para o **e-mail destinatário** definido no código. 

## Referências
- https://github.com/DanielOttodev/GoogleStorage-UploadTutorial
©️ Insper, PIBITI 2023/2024
