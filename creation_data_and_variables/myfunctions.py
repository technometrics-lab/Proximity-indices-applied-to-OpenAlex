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
import pickle
import time


## This function computes the keywords of a given paper using all functions necessary for that
def get_dico_keywords(paper,df_full): 
    
    # we first define a dictionary that we will fill in
    dicokeywords={'keyword':[],'cosine_similarity':[]}
    
    # then we choose the rows of the dataframe related to our papper
    myinfos = df_full.loc[df_full['paper']==paper].copy()
    
    #we select the text out of which we will extract our keywords
    abstract = list(set(myinfos.abstract.tolist()))
    title = list(set(myinfos.title.tolist()))
    text = str(title[0] + abstract[0])

    text_c = clean_text(text)

    # this functions get_keyword take 99.99% of the running time for each loop
    mykeywords = get_keyword(text_c)

    numberkeywords = len(mykeywords)

    # actually mykeywords is a list of tuples
    # we take every element of the list and then we take the
    # elements of the tuple we are interested in.
    for y in range(numberkeywords):
        infomykey = mykeywords[y]
        dicokeywords['keyword'].append(infomykey[0])
        dicokeywords['cosine_similarity'].append(infomykey[1])
    return dicokeywords


## This function creates a basic dataframe of citations
def create_cit_basic(listpapers,df_full): 
    
    # we first define a dictionary that we will then fill in.
    mycitationdico = {'citing_paper': [],
                      'cited_paper': [],
                      'publication_date': [],
                      'month': [],
                      'year': []
                      }
    
    #we select the rows of the dataframe related to our list of papers
    specific_paper_df = df_full.loc[listpapers]

    # We now generate our citation dico
    for paper in listpapers:
        # We select all the information we want
        myinfos = specific_paper_df.loc[[paper]]

        referenced_works = myinfos.referenced_works.tolist()
        month = list(set(myinfos.month.tolist()))
        year = list(set(myinfos.year.tolist()))
        publication_date = list(set(myinfos.publication_date.tolist()))

        numberrefwork = len(referenced_works)

        # We add the new infos the number of times there are cited work (since I want to do a dataframe)
        # we are aware that there are other ways of doing that in pandas which are more efficient.
        # nevertheless back then, we did not know anything about it, and for this reason we did it in this way. It works.
        # It's just not very efficient. We do not have the time anymore to change all the code before the end of the internship.
        mycitationdico['year'] = mycitationdico['year'] + numberrefwork * year
        mycitationdico['month'] = mycitationdico['month'] + numberrefwork * month
        mycitationdico['publication_date'] = mycitationdico['publication_date'] + numberrefwork * publication_date
        mycitationdico['citing_paper'] = mycitationdico['citing_paper'] + numberrefwork * [paper]
        mycitationdico['cited_paper'] = mycitationdico['cited_paper'] + referenced_works

    return mycitationdico


## This function returns for each paper the list of referenced papers of this paper without all papers that 
## do not belong to our list of papers (not published between 2002 and 2022 or not related to encryption technologies)
def get_references(id_paper,helpdico):
    return helpdico[id_paper]

##  this function filters the referenced works of each paper given by "filtered datat" and save it in one dictionary
def dicowithfilteredref(filtered_data):
    helpdico={}
    number_papers = len(filtered_data['id'])
    #I first fill my dictionary putting for each paper all the referenced works associated to it
    for i in range(number_papers):
        paper = filtered_data['id'][i]
        helpdico[paper] = filtered_data['referenced_works'][i]
        
    # then I filter the values of this dictionary keeping only the papers related to our studies
    for paper, ref_works in helpdico.items():
        lenrefworks = len(ref_works)
        list_refworks_commontech = []
        # for each paper, we consider each referenced work. Then we check if it is part of our keys in the dictionary
        #if it is, then it means that it is part of the papers of our studies. If it is not, then it is not part of 
        #the papers of our studies and therefore we will not keep it in the list of the referenced works for the paper in question.
        for x in range(lenrefworks):
            # I check that the referenced work is in my list of technologies
            if ref_works[x] in helpdico:
                list_refworks_commontech.append(ref_works[x])
        helpdico[paper]=list_refworks_commontech
    return helpdico

## This function takes a part of information related to a paper in filtered data and returns the list of authors
## of the paper in question (the list of OpenAlex ids) to be more specific.
def get_authors(authorships): 
    numberauthors=len(authorships)
    listauthors = []
    for u in range(numberauthors):
        listauthors.append(authorships[u]['author']['id'])
    return listauthors


## This function returns the list of authors for a specific paper taking df_full (our dataframe) as an input
def get_infos_authors(paper,df_full):
    myinfos_forauthors= df_full.loc[df_full['id']==paper].copy()
    listauthors = myinfos_forauthors.author.tolist()
    return listauthors


## This function takes a part of information related to a paper in filtered data and returns the list of scores
## of attribution to all our concepts of the paper in question (if there is no score of attribution to a certain 
## technology, then we artificially defined this missing score of attribution to be zero.
def compute_list_score(score_infos):
    # we define our list of concepts
    mylistofconcepts= ['Authentication protocol', 'Biometrics', 'Blockchain', 'Differential Privacy', 'Digital rights management',
     'Digital signature', 'Disk Encryption', 'Distributed algorithm', 'Electronic voting', 'Functional encryption',
     'Hardware acceleration', 'Hardware security module', 'Hash function', 'Homomorphic encryption',
     'Identity management', 'Key management', 'Link encryption', 'Post-quantum cryptography', 'Public-key cryptography',
     'Quantum key distribution', 'Quantum cryptography', 'Random number generation', 'Symmetric-key algorithm',
     'Threshold cryptosystem', 'Trusted Computing', 'Tunneling protocol', 'Zero-knowledge proof']
    # creating an empty dico that I will use later
    mydicofscores = {}
    list_scores = []
    
    # we first fill our dictionary with zeroes and then replace these zeroes with the information we have.
    # if we do not have any information, then it remains zero, just as wanted.
    for concept in mylistofconcepts :
        mydicofscores[concept] = 0
    
    # we go over all the concepts that are present in the part of information from filtered data
    for notion in score_infos:
        # if the concept in question is part of our list of concepts
        if notion['display_name'] in mylistofconcepts:
            # then in this case we update the value of mydicofscores
            mydicofscores[notion['display_name']] = notion['score']
        # in the other case we do not do anything since this is not our intentions
        
    # since the keys of our dico dicoofconcepts are in the order of the list of concepts
    # this is fine and we have everything in good order for further computations.
    for key, scores in mydicofscores.items():
        list_scores.append(scores)
    return list_scores


## This function recreates the abstract from an index which gives every word of the abstract and 
## what is its place in the abstract
def recreation_abstract(abstract_infos): 

    mylistofcounts = []
    # we first figure out whether we have an abstract or not
    if abstract_infos == None or abstract_infos == {}:
        myabstract = '--'
        # it means no abstract. This is cancelled anyway by the functions of text processing below which the punctuation
    else:
        #once we have an index of the abstract we recreate the abstract
        myabstract = ''
        # we first create a list of the places of all the words in the abstract
        for keywords, count in abstract_infos.items():
            mylistofcounts = mylistofcounts + count
        
        # we compute the length of the abstract and create an empty list that we will fill in progressively out 
        # with all the words present in the abstract
        lengthabstract = max(mylistofcounts) + 1  # since the count starts by zero
        listforabstract = lengthabstract * [0]
        
        #We do now put every word at the right place in the list.
        for keyword, count in abstract_infos.items():
            for index in count:
                listforabstract[index] = keyword
                
        # In the end we transform the list into the original abstract        
        for word in listforabstract:
            if word != 0 and type(word) == str:
                # We take only the words themselves without the zeroes which might still be there
                myabstract = myabstract + ' ' + str(word)
    return myabstract


## this function computes the h-index of an author based on a list of citations for each work he published
def myfunctionindex(mycitationlist): 
    if mycitationlist == []:
        return 0
        # we give 0.
    else:
        citations = np.array(mycitationlist)
        n = citations.shape[0]
        array = np.arange(1, n + 1)

        # reverse sorting
        citations = np.sort(citations)[::-1]

        # intersection of citations and k
        h_idx = np.max(np.minimum(citations, array))

        return h_idx

    
## This function returns for a list of papers a dictionary containing the paper, technological concepts
## the score of attribution of the paper to these concepts, the publication date and so on.
def create_dico_concept(listpapers,df_full):

    dicofconcepts = {'paper': [],
                     'technologies': [],
                     'score': [],
                     'publication_date': [],
                     'year': [],
                     'month': []}

    specific_paper_df = df_full.loc[listpapers].copy()
    # We create now our citation dico
    for paper in listpapers:
        # we first choose all our information
        myinfos = specific_paper_df.loc[[paper]].copy()
        concepts = myinfos.concepts.tolist()
        month = list(set(myinfos.month.tolist()))
        year = list(set(myinfos.year.tolist()))
        scores = myinfos.score_concepts.tolist()
        publication_date = list(set(myinfos.publication_date.tolist()))

        numberconcepts = len(concepts)

        # adding the new infos the number of times there are 
        # technological concepts (since we want to do a dataframe)
        dicofconcepts['year'] = dicofconcepts['year'] + numberconcepts * year
        dicofconcepts['month'] = dicofconcepts['month'] + numberconcepts * month
        dicofconcepts['paper'] = dicofconcepts['paper'] + numberconcepts * [paper]
        dicofconcepts['publication_date'] = dicofconcepts['publication_date'] + numberconcepts * publication_date
        dicofconcepts['technologies'] = dicofconcepts['technologies'] + concepts
        dicofconcepts['score'] = dicofconcepts['score'] + scores
    return dicofconcepts
    
    
## This function returns for a given list of author a pandas dataframe containing in each row several information about 
## the different kinds of H-indices, which are computed.
def compute_h_indices(listofauthor,dfauthorcit,myyears,mymonths): 
    dico_h_indices = {'author': [],
                      'year': [],
                      'month': [],
                      'yearly_H_index_notincremental': [],
                      'yearly_H_index_incremental': [],
                      'monthly_H_index_incremental': [],
                      'monthly_H_index_notincremental': []
                      }
    # we first select only the rows related to a list of authors
    specificauthorcit = dfauthorcit.loc[dfauthorcit['author'].isin(listofauthor)].copy()
    for author in listofauthor:
        # we then select the rows related a specific author
        infomyauthor = specificauthorcit.loc[specificauthorcit['author']==author].copy()
        for year in myyears:
            infosyear = infomyauthor.loc[infomyauthor['year'] == year]
            for month in mymonths:
                infosmonth = infosyear.loc[infosyear['month'] == month]
                
                # once all the subsets of the dataframe were selected, we take the information we want
                listcitfortheyear = infosmonth.citfortheyear.tolist()
                listcituptothistime_year = infosmonth.cituptothistime_year.tolist()
                listcituptothistime_month = infosmonth.cituptothistime_month.tolist()
                listcitforthemonth = infosmonth.citforthemonth.tolist()

                dico_h_indices['author'].append(author)
                dico_h_indices['year'].append(year)
                dico_h_indices['month'].append(month)
                
                #we now compute the several h-indices and add them to our dictionary
                dico_h_indices['yearly_H_index_notincremental'].append(myfunctionindex(listcitfortheyear))
                dico_h_indices['yearly_H_index_incremental'].append(myfunctionindex(listcituptothistime_year))
                dico_h_indices['monthly_H_index_incremental'].append(myfunctionindex(listcituptothistime_month))
                dico_h_indices['monthly_H_index_notincremental'].append(myfunctionindex(listcitforthemonth))
    mydf = pd.DataFrame(dico_h_indices)
    return mydf


## In this function we create a dictionary containing information such as the paper, the authors and the count of citations.
def creating_dfcit_byauthors_full(listofpaper,df_full,dfcitations):
    finalauthorcitation = {'paper': [],
                           'author': [],
                           'year': [],
                           'month': [],
                           'cituptothistime_year': [],
                           'cituptothistime_month': [],
                           'citforthemonth': [],
                           'citfortheyear': []}
    #we select the subsets of rows of the dataframe
    specificdfcit = dfcitations.loc[dfcitations['paper'].isin(listofpaper)]
    myspecificinfos = df_full.loc[df_full['paper'].isin(listofpaper)]
    
    # we now add the information for each paper we have.
    for paper in listofpaper:
        
        # we select the information for each specific paper
        infopaper = specificdfcit.loc[specificdfcit['paper']==paper]
        myinfos_forauthors= myspecificinfos.loc[myspecificinfos['paper']==paper]
        
        listauthors = myinfos_forauthors.author.tolist()

        listmonth = infopaper.month.tolist()
        listyear = infopaper.year.tolist()

        listcituptothistime_year = infopaper.cituptothistime_year.tolist()
        listcituptothistime_month = infopaper.cituptothistime_month.tolist()
        listcitfortheyear = infopaper.citfortheyear.tolist()
        listcitforthemonth = infopaper.citforthemonth.tolist()
        
        # we now add them all the right number of time to get everything right to turn it into a pandas dataframe.
        mylen = len(listmonth)

        finalauthorcitation['paper'] = finalauthorcitation['paper'] + mylen * [paper]
        finalauthorcitation['author'] = finalauthorcitation['author'] + mylen * [listauthors]

        finalauthorcitation['month'] = finalauthorcitation['month'] + listmonth
        finalauthorcitation['year'] = finalauthorcitation['year'] + listyear

        finalauthorcitation['cituptothistime_year'] = finalauthorcitation['cituptothistime_year'] + listcituptothistime_year
        finalauthorcitation['cituptothistime_month'] = finalauthorcitation['cituptothistime_month'] + listcituptothistime_month
        finalauthorcitation['citforthemonth'] = finalauthorcitation['citforthemonth'] + listcitforthemonth
        finalauthorcitation['citfortheyear'] = finalauthorcitation['citfortheyear'] + listcitfortheyear
    mydf = pd.DataFrame(finalauthorcitation)
    return mydf



## This function creates a pandas dataframe containing different kinds of counts of citations for papers
def creating_dfcit(myyears,mymonths,dfcitbasic,listofpaper): 
    finaldicocitation = {'paper': [],
                         'year': [],
                         'month': [],
                         'cituptothistime_year': [],
                         'cituptothistime_month': [],
                         'citforthemonth': [],
                         'citfortheyear': []
                         }
    #we select the subsets of rows of the dataframe
    specificpaperscit = dfcitbasic.loc[dfcitbasic['cited_paper'].isin(listofpaper)]
    for paper in listofpaper:
        
        # we select the information for each specific paper
        citingpapers = specificpaperscit.loc[specificpaperscit['cited_paper'] == paper]
        
        #we set up different variables we will use later
        mypreviousyearcit = 0
        myincrementalvalue = 0
       
        for year in myyears:
            # We reduce our selection of citing paper to the year we are considering
            # this will make everything run much faster!
            infosyear = citingpapers.loc[citingpapers['year'] == year]
            
            for month in mymonths:
                infosmonth = infosyear.loc[infosyear['month'] == month]
                
                # we compute the number of citations for this specific month
                numbercit = len(infosmonth)
                myincrementalvalue = myincrementalvalue + numbercit
                finaldicocitation['cituptothistime_month'].append(myincrementalvalue)
                finaldicocitation['citforthemonth'].append(numbercit)
                finaldicocitation['paper'].append(paper)
                finaldicocitation['year'].append(year)
                finaldicocitation['month'].append(month)
                   
                # we add the yearly information only once a year, at the end of the year.
                if month == 'December':
                    # We add 12 times the incremental value to the list of cituptothis_year citations
                    finaldicocitation['cituptothistime_year'] = \
                    finaldicocitation['cituptothistime_year'] + 12 * [myincrementalvalue]
                    
                    # For a paper, we can take cituptothistime of the end of the year -
                    # cituptothistime of the previous years, this will
                    # give us all the citations received over the year by this paper
                    citfortheyear = myincrementalvalue - mypreviousyearcit
                    finaldicocitation['citfortheyear'] = \
                    finaldicocitation['citfortheyear'] + 12 * [citfortheyear]
                    mypreviousyearcit = myincrementalvalue
                    
    # this is just to check that both lists are the same, which should be indeed the case.                
    #res = list(set(listofpaper) & set(finaldicocitation['paper']))
    #print("length common list is: "+str(len(res)))
    #print("length first list is: " + str(len(listofpaper)))
    #print("length second list is: " + str(len(list(set(finaldicocitation['paper'])))))
    
    mydf = pd.DataFrame(finaldicocitation)
    return(mydf)



snow_stemmer = SnowballStemmer(language="english")
lemmatizer = WordNetLemmatizer()
porter_stemmer = PorterStemmer()
kw_model = KeyBERT()

## all the functions below process and clean the text in order to prepare it for the keyword extraction.
## they all are quite explicit, more information and documentation can be easily found on the internet.
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

def clean_text(text): ##
    return snow_stemming(lowering(remove_punctuation(text)))

def clean_texts(texts):
    list_text = []
    for t in texts:
        list_text.append(clean_text(t))
    return list_text



def get_keyword(text): ##
    return kw_model.extract_keywords(text)


def get_keywords(texts): ##
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