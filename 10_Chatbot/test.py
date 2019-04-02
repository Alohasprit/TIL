import telegram

chii_token = '815476232:AAEq1w39JJrK7OkoUOaYgyDI6Eu_OJsJM8Y'

chii = telegram.Bot(token = chii_token)
updates = chii .getUpdates()
for u in updates:
    print(u.message)