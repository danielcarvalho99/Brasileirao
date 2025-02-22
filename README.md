# Brasileirão ⚽

Este repositório contém um pipeline de dados ELT para o processamento e análise de partidas e classificações do Campeonato Brasileiro desde 2003, início da era dos pontos corridos.

🔗 Fonte dos Dados

- Os dados utilizados neste projeto foram obtidos por meio de Web Scraping do site [GolAberto](https://www.golaberto.com.br/) 

📜 Scripts de Coleta

Na pasta **scripts**, estão os seguintes arquivos responsáveis pelo scraping dos dados:

- matches.py: Realiza o scraping das informações de partidas do Campeonato Brasileiro.
- rankings.py: Coleta os dados de classificação dos times ao longo das temporadas.

📂 Armazenamento dos Dados

Na pasta **sources**, estão armazenados os arquivos .csv gerados pelos scrapers da pasta **scripts**. Esses arquivos foram posteriormente inseridos em um Bucket S3:

- matches.csv: gerado pelo script matches.py
- rankings.csv: gerado pelo script rankings.py

⚙️ Processamento e Transformação

- etl.py: Contém o código gerado pelo AWS Glue, responsável por transformar os dados de forma adequada para análise e inseri-los em outro Bucket S3.

📌 Diagrama da Solução
- O diagrama do projeto fica da seguinte forma:
![WhatsApp Image 2024-03-28 at 19 11 39](https://github.com/danielcarvalho99/Brasileirao/assets/40178648/9299643d-0e7f-478a-84b4-1a0c6f181d2e)
