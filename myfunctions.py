# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 14:28:05 2022

@author: aless
"""

import numpy as np
import pandas as pd
from tqdm import tqdm
import re
from keybert import KeyBERT
import nltk
#nltk.download('punkt')
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
import string


# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 09:27:15 2022

@author: aless
"""

from tqdm import tqdm
import pandas as pd
import pickle
import time


def get_keywords(dico_keywords):
    list_keyword = dico_keywords['keyword']
    return list_keyword

def get_cos_sim(dico_keywords):
    list_cos_sim = dico_keywords['cosine_similarity']
    return list_cos_sim

    # I create now my citation dico
def get_dico_keywords(paper,df_full):
    dicokeywords={'keyword':[],'cosine_similarity':[]}
    myinfos = df_full.loc[df_full['paper']==paper].copy()
    abstract = list(set(myinfos.abstract.tolist()))
    title = list(set(myinfos.title.tolist()))
    text = str(title[0] + abstract[0])

    text_c = clean_text(text)

    # this functions get_keyword take 99.99% of the running time for each loop
    mykeywords = get_keyword(text_c)

    numberkeywords = len(mykeywords)

    # actually mykeywords is a list of tuples
    # I take every element of the list and then I take the
    # elements of the tuple I am interested in.
    for y in range(numberkeywords):
        infomykey = mykeywords[y]
        dicokeywords['keyword'].append(infomykey[0])
        dicokeywords['cosine_similarity'].append(infomykey[1])
    return dicokeywords


def create_keywordsdf(listpapers,df_full):
    dicokeywords = {'paper': [],
                    'keyword': [],
                    'cosine_similarity': [],
                    'publication_date': [],
                    'year': [],
                    'month': []}

    specific_paper_df = df_full.loc[listpapers].copy()
    # I create now my citation dico
    for paper in listpapers:
        myinfos = specific_paper_df.loc[[paper]].copy()
        month = list(set(myinfos.month.tolist()))
        year = list(set(myinfos.year.tolist()))
        publication_date = list(set(myinfos.publication_date.tolist()))
        abstract = list(set(myinfos.abstract.tolist()))
        title = list(set(myinfos.title.tolist()))
        text = str(title[0] + abstract[0])

        text_c = clean_text(text)

        # this functions get_keyword take 99.99% of the running time for each loop
        mykeywords = get_keyword(text_c)

        numberkeywords = len(mykeywords)

        # actually mykeywords is a list of tuples
        # I take every element of the list and then I take the
        # elements of the tuple I am interested in.
        for y in range(numberkeywords):
            infomykey = mykeywords[y]
            dicokeywords['keyword'].append(infomykey[0])
            dicokeywords['cosine_similarity'].append(infomykey[1])
            dicokeywords['paper'].append(paper)
            dicokeywords['publication_date'].append(publication_date[0])
            dicokeywords['year'].append(year[0])
            dicokeywords['month'].append(month[0])
    return dicokeywords

def create_dico_concept(listpapers,df_full):

    dicofconcepts = {'paper': [],
                     'technologies': [],
                     'score': [],
                     'publication_date': [],
                     'year': [],
                     'month': []}

    specific_paper_df = df_full.loc[listpapers].copy()
    # I create now my citation dico
    for paper in listpapers:
        myinfos = specific_paper_df.loc[[paper]].copy()
        concepts = myinfos.concepts.tolist()
        month = list(set(myinfos.month.tolist()))
        year = list(set(myinfos.year.tolist()))
        scores = myinfos.score_concepts.tolist()
        publication_date = list(set(myinfos.publication_date.tolist()))

        numberconcepts = len(concepts)

        # adding the new infos the number of times there are
        # cited work (since I want to do a dataframe)
        dicofconcepts['year'] = dicofconcepts['year'] + numberconcepts * year
        dicofconcepts['month'] = dicofconcepts['month'] + numberconcepts * month
        dicofconcepts['paper'] = dicofconcepts['paper'] + numberconcepts * [paper]
        dicofconcepts['publication_date'] = dicofconcepts['publication_date'] + numberconcepts * publication_date
        dicofconcepts['technologies'] = dicofconcepts['technologies'] + concepts
        dicofconcepts['score'] = dicofconcepts['score'] + scores
    return dicofconcepts

def create_cit_basic_noref(listpapers,df_full):
    mycitationdico = {'citing_paper': [],
                      'cited_paper': [],
                      'publication_date': [],
                      'month': [],
                      'year': []
                      }
    #time1= time.time()
    specific_paper_df = df_full.loc[listpapers].copy()
    #time2=time.time()
    #print('Time to get the sub data frame '+str(time2-time1))
    # I create now my citation dico
    for paper in listpapers:
        #time3 = time.time()
        myinfos = specific_paper_df.loc[[paper]].copy()
        #time4 = time.time()
        #print('Time to get the info for the paper '+str(time4 - time3))

        mycitingworks = myinfos.work_citing_this_paper.tolist()
        month = list(set(myinfos.month.tolist()))
        year = list(set(myinfos.year.tolist()))
        publication_date = list(set(myinfos.publication_date.tolist()))

        numbercitingworks = len(mycitingworks)

        # adding the new infos the number of times there are
        # cited work (since I want to do a dataframe)
        mycitationdico['year'] = mycitationdico['year'] + numbercitingworks * year
        mycitationdico['month'] = mycitationdico['month'] + numbercitingworks * month
        mycitationdico['publication_date'] = mycitationdico['publication_date'] + numbercitingworks * publication_date
        mycitationdico['citing_paper'] = mycitationdico['citing_paper'] + mycitingworks
        mycitationdico['cited_paper'] = mycitationdico['cited_paper'] + numbercitingworks * [paper]
        #time5 = time.time()
        #print('Time to get the info for the paper '+str(time5 - time3))
    #time6 = time.time()
    #print('Time to get one iterariont out 200 done '+str(time6 - time1))
    return mycitationdico


def create_cit_basic(listpapers,df_full):
    mycitationdico = {'citing_paper': [],
                      'cited_paper': [],
                      'publication_date': [],
                      'month': [],
                      'year': []
                      }
    #time1= time.time()
    specific_paper_df = df_full.loc[listpapers].copy()
    #time2=time.time()
    #print('Time to get the sub data frame '+str(time2-time1))
    # I create now my citation dico
    for paper in listpapers:
        #time3 = time.time()
        myinfos = specific_paper_df.loc[[paper]].copy()
        #time4 = time.time()
        #print('Time to get the info for the paper '+str(time4 - time3))

        referenced_works = myinfos.referenced_works.tolist()
        month = list(set(myinfos.month.tolist()))
        year = list(set(myinfos.year.tolist()))
        publication_date = list(set(myinfos.publication_date.tolist()))

        numberrefwork = len(referenced_works)

        # adding the new infos the number of times there are
        # cited work (since I want to do a dataframe)
        mycitationdico['year'] = mycitationdico['year'] + numberrefwork * year
        mycitationdico['month'] = mycitationdico['month'] + numberrefwork * month
        mycitationdico['publication_date'] = mycitationdico['publication_date'] + numberrefwork * publication_date
        mycitationdico['citing_paper'] = mycitationdico['citing_paper'] + numberrefwork * [paper]
        mycitationdico['cited_paper'] = mycitationdico['cited_paper'] + referenced_works
        #time5 = time.time()
        #print('Time to get the info for the paper '+str(time5 - time3))
    #time6 = time.time()
    #print('Time to get one iterariont out 200 done '+str(time6 - time1))
    return mycitationdico

def transform_to_pandas(filtered_data,helpdico,mylistofconcepts,concept_ids):
    fulldata_df = {'paper': [],
                   'title': [],
                   'publication_date': [],
                   'year': [],
                   'month': [],
                   'author': [],
                   'concepts': [],
                   'score_concepts': [],
                   'abstract': [],
                   'work_citing_this_paper':[]
                   }
    for p in filtered_data:
        # I add a list of authors for this paper
        # this will be useful later in the code
        #starting_time = time.time()
        referenced_works = helpdico[p['id']]
        citing_works =p['work_citing_this_paper']

        numberauthors = len(p['authorships'])
        numberconcepts = len(mylistofconcepts)
        numbercitingworks = len(citing_works)

        listauthors = []
        for u in range(numberauthors):
            listauthors.append(p['authorships'][u]['author']['id'])

        myabstract = recreation_abstract(p['abstract_inverted_index'])
        list_score = compute_list_score(p['concepts'], concept_ids, mylistofconcepts)

        if citing_works == []:
            numbercitingworks = 1
            citing_works = ['NaN']

        totalnumber = numberconcepts * numberauthors*numbercitingworks


        listofauthors_df = numbercitingworks*numberconcepts * listauthors

        mylistofconcepts_df = []
        list_score_df = []
        for c in range(numberconcepts):
            mylistofconcepts_df = mylistofconcepts_df +  numberauthors * [mylistofconcepts[c]]
            list_score_df = list_score_df + numberauthors * [list_score[c]]

        mylistofconcepts_df = numbercitingworks*mylistofconcepts_df
        list_score_df = numbercitingworks*list_score_df

        mycitingworks=[]
        for j in range(numbercitingworks):
            mycitingworks = mycitingworks + numberconcepts * numberauthors *[citing_works[j]]


        fulldata_df['paper'] = fulldata_df['paper'] + totalnumber * [p['id']]
        fulldata_df['title'] = fulldata_df['title'] + totalnumber * [p['title']]
        fulldata_df['year'] = fulldata_df['year'] + totalnumber * [p['year']]
        fulldata_df['month'] = fulldata_df['month'] + totalnumber * [p['month']]
        fulldata_df['publication_date'] = fulldata_df['publication_date'] + totalnumber * [p['publication_date']]
        fulldata_df['abstract'] = fulldata_df['abstract'] + totalnumber * [myabstract]

        fulldata_df['author'] = fulldata_df['author'] + listofauthors_df
        fulldata_df['concepts'] = fulldata_df['concepts'] + mylistofconcepts_df
        fulldata_df['score_concepts'] = fulldata_df['score_concepts'] + list_score_df
        fulldata_df['work_citing_this_paper'] = fulldata_df['work_citing_this_paper'] + mycitingworks

        #ending_time = time.time()
        #print('Elapsed time :' + str(ending_time - starting_time))
    return pd.DataFrame(fulldata_df)

def get_citing_works(citing_work,listpaper):
    new_citing_work=[]
    for element in citing_work:
        #print('----------')
        #print(element)
        #print(type(element))
        #print('----------')
        if str(element) in listpaper:
            new_citing_work.append(str(element))
            print('hey')
    if new_citing_work == []:
        new_citing_work = ['NaN']
    return new_citing_work

def get_references(id_paper,helpdico):
    return helpdico[id_paper]

def dicowithfilteredref(filtered_data):
    helpdico={}
    #print('creating the help dico')
    number_papers = len(filtered_data['id'])
    for i in range(number_papers):
        paper = filtered_data['id'][i]
        helpdico[paper] = filtered_data['referenced_works'][i]
    for paper, ref_works in helpdico.items():
        lenrefworks = len(ref_works)
        list_refworks_commontech = []
        for x in range(lenrefworks):
            if ref_works[x] in helpdico:
            # I check that the referenced work is in my list of technologies
                list_refworks_commontech.append(ref_works[x])
        helpdico[paper]=list_refworks_commontech
    return helpdico

def get_authors(authorships):
    # authorships = paper['authorships'] ici
    numberauthors=len(authorships)
    listauthors = []
    for u in range(numberauthors):
        listauthors.append(authorships[u]['author']['id'])
    return listauthors


def get_infos_authors(paper,df_full):
    myinfos_forauthors= df_full.loc[df_full['id']==paper].copy()
    listauthors = myinfos_forauthors.author.tolist()
    return listauthors

def compute_list_score(score_infos):
    mylistofconcepts= ['Authentication protocol', 'Biometrics', 'Blockchain', 'Differential Privacy', 'Digital rights management',
     'Digital signature', 'Disk Encryption', 'Distributed algorithm', 'Electronic voting', 'Functional encryption',
     'Hardware acceleration', 'Hardware security module', 'Hash function', 'Homomorphic encryption',
     'Identity management', 'Key management', 'Link encryption', 'Post-quantum cryptography', 'Public-key cryptography',
     'Quantum key distribution', 'Quantum cryptography', 'Random number generation', 'Symmetric-key algorithm',
     'Threshold cryptosystem', 'Trusted Computing', 'Tunneling protocol', 'Zero-knowledge proof']
    #score_infos = paper['concepts'] ici
    mydicofscores = {}
    list_scores = []
    # creating an empty dico that I will use later
    for concept in mylistofconcepts :
        mydicofscores[concept] = 0

    for notion in score_infos:
        if notion['display_name'] in mylistofconcepts:
            # in this case I update the value of mydicofscores
            mydicofscores[notion['display_name']] = notion['score']
    # since the keys of my dico dicoofconcepts are in the order of the list of concepts
    # this is fine and I have everything in good order! I put the score in my dico of concepts
    for key, scores in mydicofscores.items():
        list_scores.append(scores)
    return list_scores

def recreation_abstract(abstract_infos):
    # abstract_infos = paper['abstract_inverted_index'] ici
    mylistofcounts = []
    if abstract_infos == None or abstract_infos == {}:
        myabstract = '--'
        # it means no abstract. This is cancelled anyway by Jacques functions
    else:
        myabstract = ''
        for keywords, count in abstract_infos.items():
            mylistofcounts = mylistofcounts + count

        lengthabstract = max(mylistofcounts) + 1  # since the count starts by zero
        listforabstract = lengthabstract * [0]
        for keyword, count in abstract_infos.items():
            for index in count:
                listforabstract[index] = keyword
        for word in listforabstract:
            if word != 0 and type(word) == str:
                # I take only the words themselves
                # the zeroes are not what I want of course
                myabstract = myabstract + ' ' + str(word)
    return myabstract


def transform_to_pandas_ref(filtered_data,helpdico,mylistofconcepts,concept_ids):
    fulldata_df = {'paper': [],
                   'title': [],
                   'publication_date': [],
                   'year': [],
                   'month': [],
                   'author': [],
                   'referenced_work': [],
                   'concepts': [],
                   'score_concepts': [],
                   'abstract': []
                   }
    for p in filtered_data:
        # I add a list of authors for this paper
        # this will be useful later in the code
        #starting_time = time.time()
        referenced_works = helpdico[p['id']]
        citing_works =p['work_citing_this_paper']

        numberauthors = len(p['authorships'])
        numberrefwork = len(referenced_works)
        numberconcepts = len(mylistofconcepts)

        listauthors = []
        for u in range(numberauthors):
            listauthors.append(p['authorships'][u]['author']['id'])

        myabstract = recreation_abstract(p['abstract_inverted_index'])
        list_score = compute_list_score(p['concepts'], concept_ids, mylistofconcepts)

        if referenced_works == []:
            numberrefwork = 1
            referenced_works = ['NaN']

        totalnumber = numberrefwork * numberconcepts * numberauthors

        listofauthors_1 = []
        for b in range(numberauthors):
            listofauthors_1 = listofauthors_1 + numberrefwork * [listauthors[b]]

        listofauthors_df = numberconcepts * listofauthors_1

        mylistofconcepts_df = []
        list_score_df = []
        for c in range(numberconcepts):
            mylistofconcepts_df = mylistofconcepts_df + numberrefwork * numberauthors * [mylistofconcepts[c]]
            list_score_df = list_score_df + numberrefwork * numberauthors * [list_score[c]]

        mylistofconcepts_df = mylistofconcepts_df
        list_score_df = list_score_df


        fulldata_df['paper'] = fulldata_df['paper'] + totalnumber * [p['id']]
        fulldata_df['title'] = fulldata_df['title'] + totalnumber * [p['title']]
        fulldata_df['year'] = fulldata_df['year'] + totalnumber * [p['year']]
        fulldata_df['month'] = fulldata_df['month'] + totalnumber * [p['month']]
        fulldata_df['publication_date'] = fulldata_df['publication_date'] + totalnumber * [p['publication_date']]
        fulldata_df['abstract'] = fulldata_df['abstract'] + totalnumber * [myabstract]
        fulldata_df['referenced_work'] = fulldata_df['referenced_work'] + numberconcepts * numberauthors * referenced_works

        fulldata_df['author'] = fulldata_df['author'] + listofauthors_df
        fulldata_df['concepts'] = fulldata_df['concepts'] + mylistofconcepts_df
        fulldata_df['score_concepts'] = fulldata_df['score_concepts'] + list_score_df

        #ending_time = time.time()
        #print('Elapsed time :' + str(ending_time - starting_time))
    return fulldata_df




def myfunctionindex(mycitationlist):
    if mycitationlist == []:
        return 0
        # we give 0 and we might change this later in the computations if necessary.
    else:
        citations = np.array(mycitationlist)
        n = citations.shape[0]
        array = np.arange(1, n + 1)

        # reverse sorting
        citations = np.sort(citations)[::-1]

        # intersection of citations and k
        h_idx = np.max(np.minimum(citations, array))

        return h_idx

def compute_h_indices(listofauthor,dfauthorcit,myyears,mymonths):
    dico_h_indices = {'author': [],
                      'year': [],
                      'month': [],
                      'yearly_H_index_notincremental': [],
                      'yearly_H_index_incremental': [],
                      'monthly_H_index_incremental': [],
                      'monthly_H_index_notincremental': []
                      }

    specificauthorcit = dfauthorcit.loc[dfauthorcit['author'].isin(listofauthor)].copy()
    for author in listofauthor:
        # find a way like for last doc to change this line of code
        # it takes 98% of the time for each iteration of the loop
        infomyauthor = specificauthorcit.loc[specificauthorcit['author']==author].copy()
        for year in myyears:
            infosyear = infomyauthor.loc[infomyauthor['year'] == year]
            for month in mymonths:
                infosmonth = infosyear.loc[infosyear['month'] == month]

                listcitfortheyear = infosmonth.citfortheyear.tolist()
                listcituptothistime_year = infosmonth.cituptothistime_year.tolist()
                listcituptothistime_month = infosmonth.cituptothistime_month.tolist()
                listcitforthemonth = infosmonth.citforthemonth.tolist()

                dico_h_indices['author'].append(author)
                dico_h_indices['year'].append(year)
                dico_h_indices['month'].append(month)

                dico_h_indices['yearly_H_index_notincremental'].append(myfunctionindex(listcitfortheyear))
                dico_h_indices['yearly_H_index_incremental'].append(myfunctionindex(listcituptothistime_year))
                dico_h_indices['monthly_H_index_incremental'].append(myfunctionindex(listcituptothistime_month))
                dico_h_indices['monthly_H_index_notincremental'].append(myfunctionindex(listcitforthemonth))
    mydf = pd.DataFrame(dico_h_indices)
    return mydf


def creating_dfcit_byauthors_full(listofpaper,df_full,dfcitations):
    finalauthorcitation = {'paper': [],
                           'author': [],
                           'year': [],
                           'month': [],
                           'cituptothistime_year': [],
                           'cituptothistime_month': [],
                           'citforthemonth': [],
                           'citfortheyear': []}
    specificdfcit = dfcitations.loc[dfcitations['paper'].isin(listofpaper)]
    myspecificinfos = df_full.loc[df_full['paper'].isin(listofpaper)]
    for paper in listofpaper:
        infopaper = specificdfcit.loc[specificdfcit['paper']==paper].copy()
        myinfos_forauthors= myspecificinfos.loc[myspecificinfos['paper']==paper].copy()

        # all the lists I need
        listauthors = myinfos_forauthors.author.tolist()

        listmonth = infopaper.month.tolist()
        listyear = infopaper.year.tolist()

        listcituptothistime_year = infopaper.cituptothistime_year.tolist()
        listcituptothistime_month = infopaper.cituptothistime_month.tolist()
        listcitfortheyear = infopaper.citfortheyear.tolist()
        listcitforthemonth = infopaper.citforthemonth.tolist()
        mylen = len(listmonth)

        finalauthorcitation['paper'] = finalauthorcitation['paper'] + mylen * [paper]
        finalauthorcitation['author'] = finalauthorcitation['author'] + mylen * [listauthors]

        finalauthorcitation['month'] = finalauthorcitation['month'] + listmonth
        finalauthorcitation['year'] = finalauthorcitation['year'] + listyear

        finalauthorcitation['cituptothistime_year'] = finalauthorcitation['cituptothistime_year'] \
                                                          + listcituptothistime_year
        finalauthorcitation['cituptothistime_month'] = finalauthorcitation['cituptothistime_month'] \
                                                           + listcituptothistime_month
        finalauthorcitation['citforthemonth'] = finalauthorcitation['citforthemonth'] + listcitforthemonth
        finalauthorcitation['citfortheyear'] = finalauthorcitation['citfortheyear'] + listcitfortheyear
    mydf = pd.DataFrame(finalauthorcitation)
    return mydf


def creating_dfcit_byauthors(listofpaper,df_full,dfcitations):
    finalauthorcitation = {'paper': [],
                           'author': [],
                           'year': [],
                           'month': [],
                           'cituptothistime_year': [],
                           'cituptothistime_month': [],
                           'citforthemonth': [],
                           'citfortheyear': []}
    specificdfcit = dfcitations.loc[listofpaper].copy()
    myspecificinfos = df_full.loc[listofpaper].copy()
    for paper in listofpaper:
        infopaper = specificdfcit.loc[[paper]].copy()
        myinfos_forauthors= myspecificinfos.loc[[paper]].copy()

        # all the lists I need
        listauthors = myinfos_forauthors.author.tolist()

        listmonth = infopaper.month.tolist()
        listyear = infopaper.year.tolist()

        listcituptothistime_year = infopaper.cituptothistime_year.tolist()
        listcituptothistime_month = infopaper.cituptothistime_month.tolist()
        listcitfortheyear = infopaper.citfortheyear.tolist()
        listcitforthemonth = infopaper.citforthemonth.tolist()
        mylen = len(listmonth)

        # I obtain a dataframe and I want only a list of authors
        for author in listauthors:
            finalauthorcitation['paper'] = finalauthorcitation['paper'] + mylen * [paper]
            finalauthorcitation['author'] = finalauthorcitation['author'] + mylen * [author]

            finalauthorcitation['month'] = finalauthorcitation['month'] + listmonth
            finalauthorcitation['year'] = finalauthorcitation['year'] + listyear

            finalauthorcitation['cituptothistime_year'] = finalauthorcitation['cituptothistime_year'] \
                                                          + listcituptothistime_year
            finalauthorcitation['cituptothistime_month'] = finalauthorcitation['cituptothistime_month'] \
                                                           + listcituptothistime_month
            finalauthorcitation['citforthemonth'] = finalauthorcitation['citforthemonth'] + listcitforthemonth
            finalauthorcitation['citfortheyear'] = finalauthorcitation['citfortheyear'] + listcitfortheyear
    return finalauthorcitation


def creating_dfcit(myyears,mymonths,dfcitbasic,listofpaper):
    finaldicocitation = {'paper': [],
                         'year': [],
                         'month': [],
                         'cituptothistime_year': [],
                         'cituptothistime_month': [],
                         'citforthemonth': [],
                         'citfortheyear': []
                         }
    specificpaperscit = dfcitbasic.loc[dfcitbasic['cited_paper'].isin(listofpaper)].copy()
    for paper in listofpaper:
        # finaldicocitation['citfortheyear'].append(1)
        # finaldicocitation['cituptothistime_year'].append(1)
        # finaldicocitation['cituptothistime_month'].append(1)
        # finaldicocitation['citforthemonth'].append(1)
        # finaldicocitation['paper'].append(paper)
        # finaldicocitation['year'].append(1)
        # finaldicocitation['month'].append(1)

        mypreviousyearcit = 0
        myincrementalvalue = 0
        # I want to increment the value of citations in 'cituptothistime'
        citingpapers = specificpaperscit.loc[specificpaperscit['cited_paper'] == paper].copy()
        #print(citingpapers.year.tolist())
        for year in myyears:
            # I reduce my selection of citing paper to the year I am considering
            # this will make everything run much faster!
            infosyear = citingpapers.loc[citingpapers['year'] == year].copy()
            for month in mymonths:
                infosmonth = infosyear.loc[infosyear['month'] == month].copy()
                # we compute the number of citations for this specific month
                numbercit = len(infosmonth)
                myincrementalvalue = myincrementalvalue + numbercit
                finaldicocitation['cituptothistime_month'].append(myincrementalvalue)
                finaldicocitation['citforthemonth'].append(numbercit)
                finaldicocitation['paper'].append(paper)
                finaldicocitation['year'].append(year)
                finaldicocitation['month'].append(month)

                if month == 'December':
                    # I add 12 times my incremental value to the list of cituptothis_year citations
                    finaldicocitation['cituptothistime_year'] = \
                    finaldicocitation['cituptothistime_year'] + 12 * [myincrementalvalue]
                    # For a paper I can take cituptothistime of the end of the year -
                    # cituptothistime of the previous years, this will
                    # give me all the citations received over the year by this paper
                    citfortheyear = myincrementalvalue - mypreviousyearcit
                    finaldicocitation['citfortheyear'] = \
                    finaldicocitation['citfortheyear'] + 12 * [citfortheyear]
                    mypreviousyearcit = myincrementalvalue
    res = list(set(listofpaper) & set(finaldicocitation['paper']))
    print("length common list is: "+str(len(res)))
    print("length first list is: " + str(len(listofpaper)))
    print("length second list is: " + str(len(list(set(finaldicocitation['paper'])))))
    mydf = pd.DataFrame(finaldicocitation)
    return(mydf)
    #mydf.to_pickle(file_name)




# we are computing the H-index on the basis of the paper there are on openalex
# and that are related to these technologies (encryption technologies), 
# not necessarily the H-index overall written paper of the author
# justify this choice in the paper. 



snow_stemmer = SnowballStemmer(language="english")
lemmatizer = WordNetLemmatizer()
porter_stemmer = PorterStemmer()
kw_model = KeyBERT()


def tokenization(text):
    text_token = nltk.tokenize.word_tokenize(text)
    return text_token

def remove_punctuation(text):
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    text_filtre = regex.sub(repl=" ", string=str(text))
    text_token = tokenization(text_filtre)
    text_w_p = " ".join([i for i in text_token if i not in string.punctuation])
    return text_w_p

def lowering(text):
    text_lower = (lambda x: x.lower())(text)
    return text_lower

def snow_stemming(text):
    text_token = tokenization(text)
    text_stem = [snow_stemmer.stem(word) for word in text_token]
    sentence_clean = ' '.join(w for w in text_stem)
    return sentence_clean

def clean_text(text):
    return snow_stemming(lowering(remove_punctuation(text)))

def clean_texts(texts):
    list_text = []
    for t in texts:
        list_text.append(clean_text(t))
    return list_text



def get_keyword(text):
    return kw_model.extract_keywords(text)


def get_keywords(texts):
    keywords_per_doc = list()
    
    for t in tqdm(texts):
        keywords_per_doc.append(kw_model.extract_keywords(t))
    
    return keywords_per_doc


def get_weighted_list(keywords_per_doc):
    
    keywords = list()
    keywords_val = list()

    for kw_p_d in keywords_per_doc : 
        for kw, val in kw_p_d:
            if kw not in keywords:
                keywords.append(kw)
                keywords_val.append(val)
            else :
                for i in range(len(keywords_val)):
                    if kw == keywords[i]:
                        new_val = val + keywords_val[i]
                        keywords_val[i] = new_val
                        break
    
    val = list()
    for i in keywords_val:
        val.append(round(i / len(keywords_per_doc), 4))
        
    res = pd.DataFrame(list(zip(keywords, val)), columns=["keywords", "values"])
    res.sort_values(by = "values", ascending = False, inplace = True)
    res.reset_index(drop=True, inplace=True)
    
    return res