cd scraping/lib/python3.8/site-packages
sudo zip -r9 ../../../../function.zip .
cd ../../../../
sudo zip -g function.zip -r app
# 以下はアメリカリージョン
# aws --region us-east-1 lambda update-function-code --function-name kpopScrapingFunc --zip-file fileb://function.zip
# 以下は東京リージョン
aws --region ap-northeast-1 lambda update-function-code --function-name kpopScrapingFunc --zip-file fileb://function.zip