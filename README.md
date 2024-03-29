# Brasileirão

Este é um projeto de engenharia de dados, utilizando a AWS como serviço de nuvem, responsável por extrair e estruturar dados de partidas e classificações dos times do campeonato brasileiro desde o início da era dos pontos corridos, em 2003.

As ferramentas utilizadas nesse projeto foram:
* BeautifulSoup: Biblioteca em Python utilizada para Web Scraping, coletando informações do HTML do site [GolAberto](https://www.golaberto.com.br/)
* AWS S3: Os buckets da AWS foram utlizados para o armazenamento tanto dos dados brutos, quanto dos dados após o ETL
* AWS GLUE: Responsável pela geração dos Schemas das tabelas e geração dos catálogos


A arquitetura do projeto fica da seguinte forma:
![WhatsApp Image 2024-03-28 at 19 11 39](https://github.com/danielcarvalho99/Brasileirao/assets/40178648/9299643d-0e7f-478a-84b4-1a0c6f181d2e)
