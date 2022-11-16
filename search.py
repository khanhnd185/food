import json
from tracemalloc import start
import requests as r
import logging

HOST = "localhost"
PORT = "8983"
CORE = "food"

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

def SendRequestToSolr(q, s):
    qt         = "select"
    url        = 'http://' + HOST + ':' + PORT + '/solr/' + CORE + '/' + qt + '?'
    q          = "q=ingredients%3A" + q
    wt         = "wt=json"
    rows       = "rows=10"
    start      = "start={}".format(s)
    indent     = "indent=true"
    params     = [indent, q, wt, start]
    p          = "&".join(params)
    ret = r.get(url+p, headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"})

    if ret.status_code == 200:
        return json.loads(ret.content)
    else:
        return {"response":{"numFound":0}}


def GetFoodFromIngredient(ing):
    ret = SendRequestToSolr(ing, 0)
    num = ret['response']['numFound']
    stt = 0
    recipes = {}

    while stt < num:
        ret = SendRequestToSolr(ing, stt)
        search_results = ret['response']['docs']

        for result in search_results:
            recipes[result["id"]] = result

        stt = stt + len(search_results)

    logger.info('Get {} for keyword {}'.format(len(recipes), ing))

    return recipes        


def MergeDict(d1: dict, d2: dict):
    d = {}

    for k, v in d1.items():
        if k in d2.keys():
            d[k] = v

    logger.info('Get {} merge from {} and {}'.format(len(d.keys()), len(d1.keys()), len(d2.keys())))

    return d

def GetFoodFromIngredients(keywords):
    ingredients = keywords.split(', ')
    logger.info('Get ingredients {}'.format(ingredients))
    recipes = {}
    start_loop = True

    for ingredient in ingredients:
        ret = GetFoodFromIngredient(ingredient)

        if start_loop == True:
            start_loop = False
            recipes = ret
        else:
            recipes = MergeDict(recipes, ret)
            
        if recipes == {}:
            break

    logger.info('Get recipes {}'.format(len(recipes.keys())))

    return list(recipes.values())


if __name__=="__main__":
    ret = GetFoodFromIngredients("apple")
    print(len(ret.keys()))
