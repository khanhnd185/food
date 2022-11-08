import pandas as pd
import json
import requests as r
import streamlit as st

st.markdown('<h1 style="background-color: gainsboro; padding-left: 10px; padding-bottom: 20px;">Food Search Engine</h1>', unsafe_allow_html=True)
query = st.text_input('', help='Enter the ingredients and hit Enter/Return')
query = query.replace(" ", "+") #replacing the spaces in query result with +

def get_query(i1, i2):
    host       = "localhost"
    port       = "8983"
    core       = "food"
    qt         = "select"
    url        = 'http://' + host + ':' + port + '/solr/' + core + '/' + qt + '?'


    q          = "q=ingredients%3A" + i1
    wt         = "wt=json"
    #wt        = "wt=python"
    rows       = "rows=10"
    indent     = "indent=true"
    if i2 != None:
        op         = "q.op=AND"
        fq         = "fq=ingredients%3A" + i2
        params     = [fq, indent, op, q, wt]
    else:
        params     = [indent, q, wt]

    p          = "&".join(params)

    return url+p



if query: #Activates the code below on hitting Enter/Return in the search textbox
    try:#Exception handling
        ingredients = query.split(', ')
        if len(ingredients) == 0:
            raise Exception("No result")
        elif len(ingredients) == 1:
            i1 = ingredients[0]
            i2 = None
        else:
            i1, i2 = ingredients[:2]

        req = r.get(get_query(i1, i2),
                    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"})
        result_str = '<html><table style="border: none;">' #Initializing the HTML code for displaying search results
        
        if req.status_code == 200: #Status code 200 indicates a successful request
            js = json.loads(req.content)
            search_result = js['response']['docs']
            result_df = pd.DataFrame() #Initializing the data frame that stores the results
            
            for n,i in enumerate(search_result): #iterating through the search results
                url_txt = i['title'][0]
                href = i['url'][0]
                description = " ".join(i['ingredients'])
                cite = "Calo: {} ".format(i['calo'][0])

                result_df = result_df.append(pd.DataFrame({"Title": url_txt, "URL": href, "Description": description}, index=[n]))
                count_str = f'<b style="font-size:20px;">Food Search returned {len(result_df)} results</b>'
                ########################################################
                ######### HTML code to display search results ##########
                ########################################################
                result_str += f'<tr style="border: none;"><h3><a href="{href}" target="_blank">{url_txt}</a></h3></tr>'+\
                f'<tr style="border: none;"><strong style="color:green;">{cite}</strong></tr>'+\
                f'<tr style="border: none;">{description}</tr>'+\
                f'<tr style="border: none;"><td style="border: none;"></td></tr>'
            result_str += '</table></html>'
            
        #if the status code of the request isn't 200, then an error message is displayed along with an empty data frame        
        else:
            result_df = pd.DataFrame({"Title": "", "URL": "", "Description": ""}, index=[0])
            result_str = '<html></html>'
            count_str = '<b style="font-size:20px;">Looks like an error!!</b>'
            
    #if an exception is raised, then an error message is displayed along with an empty data frame
    except:
        result_df = pd.DataFrame({"Title": "", "URL": "", "Description": ""}, index=[0])
        result_str = '<html></html>'
        count_str = '<b style="font-size:20px;">Looks like an error!!</b>'
    
    st.markdown(f'{count_str}', unsafe_allow_html=True)
    st.markdown(f'{result_str}', unsafe_allow_html=True)
    st.markdown('<h3>Data Frame of the above search result</h3>', unsafe_allow_html=True)
    st.dataframe(result_df)
