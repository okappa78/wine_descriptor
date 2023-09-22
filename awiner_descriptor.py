import pandas as pd
import openai
import time

path = #path_to_file

wine_list = pd.read_excel(path)

cols = ['REGIÃO', 'TIPO', 'PRODUTOR', 'PRODUTO', 'COLHEITA']
wine_list['FULL_TITLE'] = wine_list[cols].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
wine_list.dropna(subset=['PRODUTO'], inplace=True)

wine_list['DESCRIPTION'] = None
wine_list['DESCRIPTION_rus'] = None


def get_description(wine_name, lang):
    api_key = #api_key

    wine_template = "type (like red dry or white sweet or smth else), alcohol, grapes, style, flavour, food goes with, temperature serve"
    cht_req = f"""give me description of this wine {wine_name} in {lang} according to this template: {wine_template}"""

    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Вы - пользователь"},
            {"role": "user", "content": cht_req}
        ],
        max_tokens=350,  # Ограничение количества токенов в ответе
        n=1,  # Получить 1 альтернативных ответа
        stop=None,  # Модель остановится после этой фразы
        temperature=0.3  # Установка температуры для контроля случайности
        # 1 - более случайной и креативной; 0 - одель будет более предсказуемой и фокусированной
    )

    return response.choices[0].message.content

for i in wine_list.index:
    wine_name = wine_list.loc[i, 'FULL_TITLE']
    wine_list.loc[i, 'DESCRIPTION'] = get_description(wine_name, 'english')
    wine_list.loc[i, 'DESCRIPTION_rus'] = get_description(wine_name, 'russian')
    time.sleep(60)

wine_list.to_excel(#path_outfile)