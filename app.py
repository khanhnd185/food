import pandas as pd
import streamlit as st
from search import GetFoodFromIngredients
from anticancer import GetHealthyScore

st.markdown('<h1 style="background-color: gainsboro; padding-left: 10px; padding-bottom: 20px;">Food Search Engine</h1>', unsafe_allow_html=True)
query = st.text_input('', help='Enter the ingredients and hit Enter/Return')

option = st.selectbox(
    'Sorted by?',
    ("User rating", 'Anticancer score', 'Calories', 'Fat', "Protein"))

sorted_by = {
    'Anticancer score':'anticancer',
    'Calories': 'calo',
    'Fat': 'fat',
    'User rating': 'rate',
    'Protein': 'prot'
}[option]

if query:
    try:
        recipes = GetFoodFromIngredients(query)
        result_str = '<html><table style="border: none;">'
        
        if len(recipes) > 0:
            scores = []

            for r in recipes:
                if sorted_by == 'anticancer':
                    score = GetHealthyScore(r['ingredients'])
                else:
                    ## Exception
                    if sorted_by not in r.keys():
                        r[sorted_by] = [4.0]

                    score = r[sorted_by][0]
                scores.append(score)

            index = sorted(range(len(scores)), reverse=True, key=lambda k: scores[k])
            
            for n in index:
                i = recipes[n]
                url_txt = i['title'][0]
                href = i['url'][0]
                description = " ".join(i['ingredients'])
                score = GetHealthyScore(i['ingredients'])
                cite = "{}: {} ".format(option, scores[n])

                result_str += f'<tr style="border: none;"><h3><a href="{href}" target="_blank">{url_txt}</a></h3></tr>'+\
                f'<tr style="border: none;"><strong style="color:green;">{cite}</strong></tr>'+\
                f'<tr style="border: none;">{description}</tr>'+\
                f'<tr style="border: none;"><td style="border: none;"></td></tr>'
            count_str = f'<b style="font-size:20px;">Food Search returned {len(recipes)} results</b>'
            result_str += '</table></html>'


        else:
            result_str = '<html></html>'
            count_str = '<b style="font-size:20px;">There is no result for the input!</b>'

    except:
        result_str = '<html></html>'
        count_str = '<b style="font-size:20px;">Looks like an error!!</b>'
    
    st.markdown(f'{count_str}', unsafe_allow_html=True)
    st.markdown(f'{result_str}', unsafe_allow_html=True)
