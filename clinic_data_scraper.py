# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 16:34:27 2024

@author: stan

This script is an example of data scraping for the site https://www.dentaldepartures.com/dentist/supreme-dental-clinic .
This script extract all clinics and associated city for a provided country
This script use an accessible backend API to extract data
Disclamer:
This code is for educational/demonstrative purposes, and stated that I have no affiliation with the site and that neither 
I nor the software would be held liable for any consequences resulting from its use. 
"""

import requests

            #############################
            #                           #
            # Parameters Initialization #
            #                           #
            #############################
            
COUNTRY='mexico' #This parameter is used as a country filter in the API query 
PAGE_SIZE=600    #This parameter is used to setup the number of data extracted for each call. The first page is limited to 10
PAGE=1           #This parameter is used to setup th start page used in the script
FILENAME="mexico_extract.csv" # This parameter is used to define the output filename



all_clinic=[]    #Initliaze an empty list which will store all clinic data


            #############################
            #                           #
            #     Usefull Functions     #
            #                           #
            #############################


def convert_to_csv(data):
    """
    A function that convert a provided table to a csv
    This function is used in the script to convert extracted data stored in a list to a csv format
    """
    csv_data = ""
    for row in data:
        csv_data += ",".join(map(str, row)) + "\n"
    return csv_data


            #############################
            #                           #
            #     Data Extraction       #
            #                           #
            #############################


end=False #This flag is used to monitor if all data are extracted

while(not(end))  :
    #BACKEND URL usedby dentaldepartures to get data
    API_URL = "https://stagl-api.medicaldepartures.com/keendex/v1/static-clinic-search?treatment=&country=mexico&province=&city=&page="+str(PAGE)+"&size="+str(PAGE_SIZE)+"&sort=recommended"
    if PAGE==1:
        size=10
    else:
        size=600


    #Initilize the query API header query
    headers = {
        "Origin": "https://www.dentaldepartures.com",
        "Referer":"https://www.dentaldepartures.com/",
        "X-SITE-ID":"1"
               
    }
    
    #Send the query to get data
    response = requests.get(API_URL, headers=headers) 
    
    #Check if the query is a success and if the response is empty
    
    if( response.status_code ==200 and 'res' in response.json()  and len(response.json()['res']['search_result'])>0):
        all_result=response.json()['res']['search_result']
    else:
        end=True
    if(not end):
        if response.status_code == 200:
         
            #Parse response json to extract clinic name and associated city
            for i in range(len(all_result)):     
                name=all_result[i]['name']
                if len(all_result[i]['i18n'][0])>0:
                    try:
                        city=all_result[i]['i18n'][0]['location']['city']['name']
                    except:
                        city='NO INFO' #If the City is empty we replace it by NO INFO
                 
                    all_clinic.append([name,city])
                else:
                    all_clinic.append([name,'NO INFO'])
           
        else:
           
            print("The query failed, error code :", response.status_code)
        
        PAGE+=1




# Remove Duplicate
unique_tuples = set(tuple(row) for row in all_clinic)

# Convert the unique tuples back to lists
all_clinic = [list(row) for row in unique_tuples]

# Add title for each column in CSV
csv_with_title = "Clinic Name,City\n" + convert_to_csv(all_clinic[1:])  # Skip the first row


#Save data in the file with the provided filename
with open(FILENAME, "w",encoding='utf-8') as f:
   f.write(csv_with_title)