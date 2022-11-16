import pandas as pd
import streamlit as st
from search import GetFoodFromIngredients

st.markdown('<h1 style="background-color: gainsboro; padding-left: 10px; padding-bottom: 20px;">Food Search Engine</h1>', unsafe_allow_html=True)
query = st.text_input('', help='Enter the ingredients and hit Enter/Return')


if query:
    try:
        recipes = GetFoodFromIngredients(query)
        result_str = '<html><table style="border: none;">'
        
        if len(recipes) > 0:
            result_df = []
            
            for n,i in enumerate(recipes):
                url_txt = i['title'][0]
                href = i['url'][0]
                description = " ".join(i['ingredients'])
                cite = "Calo: {} ".format(i['calo'][0])

                result_df.append(pd.DataFrame({"Title": url_txt, "URL": href, "Description": description}, index=[n]))
                count_str = f'<b style="font-size:20px;">Food Search returned {len(result_df)} results</b>'
                result_str += f'<tr style="border: none;"><h3><a href="{href}" target="_blank">{url_txt}</a></h3></tr>'+\
                f'<tr style="border: none;"><strong style="color:green;">{cite}</strong></tr>'+\
                f'<tr style="border: none;">{description}</tr>'+\
                f'<tr style="border: none;"><td style="border: none;"></td></tr>'
            result_str += '</table></html>'

            result_df = pd.DataFrame.from_records(result_df)

        else:
            result_df = pd.DataFrame({"Title": "", "URL": "", "Description": ""}, index=[0])
            result_str = '<html></html>'
            count_str = '<b style="font-size:20px;">Looks like an error!!</b>'

    except:
        result_df = pd.DataFrame({"Title": "", "URL": "", "Description": ""}, index=[0])
        result_str = '<html></html>'
        count_str = '<b style="font-size:20px;">Looks like an error!!</b>'
    
    st.markdown(f'{count_str}', unsafe_allow_html=True)
    st.markdown(f'{result_str}', unsafe_allow_html=True)
    st.markdown('<h3>Data Frame of the above search result</h3>', unsafe_allow_html=True)
    st.dataframe(result_df)
