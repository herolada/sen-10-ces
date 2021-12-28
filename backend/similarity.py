import requests
import json

URL = "https://api.twinword.com/api/text/similarity/latest/"
HEADERS = {
    'content-type': "application/x-www-form-urlencoded",
    'x-rapidapi-host': "twinword-text-similarity-v1.p.rapidapi.com",
    'x-rapidapi-key': "HHUH3/4u13AyN87Yx660O04XUqe7FNT+hMDQ2QwSOFSigeqZNpgKXtPzF8hjUbMgDTYGzUW2vLhJIC3oSl+vqQ==",
    'X-Twaip-Key': "HHUH3/4u13AyN87Yx660O04XUqe7FNT+hMDQ2QwSOFSigeqZNpgKXtPzF8hjUbMgDTYGzUW2vLhJIC3oSl+vqQ=="
    }

def score2text(score):
    if score is None:
        score = 0
    score = round(10*score)
    texts = ["That's absolute garbage...",
            "Embarasing...",
            "What a poor translation...",
            "At least you got the language correct.",
            "Not so awful.",
            "You tried.",
            "That was not bad.",
            "Nice try!",
            "Very close!",
            "Amazing!",
            "ABSOLUTELY PERFECT!!!"]
    return(texts[score])


def get_similarity(text1,text2):
    payload = "text1={t1}&text2={t2}".format(t1=text1, t2=text2)
    payload = payload.encode("utf-8")
    response = requests.request("POST", URL, data=payload, headers=HEADERS)
    similarity = response.json().get('similarity')
    return(score2text(similarity))