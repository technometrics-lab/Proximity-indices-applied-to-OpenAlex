# Content of the folder: creation_data_and_variables

<a name="readme-top"></a>

This folder contains all the files which create the different pandas dataframes of variables. We explain below the function of each file 
and in the order they are run in directory_file_creation_data:

* scraping_data_from_Open_Alex
 <br> This file downloads all the data related to our list of concepts present on OpenAlex making a request.
 
* filtering_data
 <br> This file filters the raw data obtained in the previous file. On the one hand it takes only the information we want while
 on the other hand it eliminates all papers which do not correspond to our research. For example, it takes only the paper published 
 between 2002 and 2022, papers which present authors and a title, etc.
 
* data_to_pandas
 <br> This file transforms the filtered data obtained above in a pandas dataframe.
 
 * dfcitbasic
 <br> This file creates a database of citations.
 This has the form of a dataframe with these columns: 'citing_paper', 'cited_paper', 'publication_date', 'month', 'year'.
 
 * dfkeywords
 <br> This file extracts all the keywords from the titles and the abstract of the papers and turns it into a database of keywords.
 This has the form of a dataframe with these columns: 'paper', 'keyword', 'cosine_similarity', 'publication_date', 'year', 'month'.
 
 * dfconcepts
 <br> This file creates a database of containing all the information about the concepts and the score of attribution to concepts.
  This has the form of a dataframe with these columns: 'paper', 'technologies', 'score', 'publication_date', 'year', 'month'.
 
 * dffinalcit
 <br> This file creates a database of citations count. This has the form of a dataframe with these columns: 'paper', 'year', 'month', 
 'cituptothistime_year', 'cituptothistime_month', 'citforthemonth', 'citfortheyear'.
 
 * dfcit_author
 <br> This file simply adds a column 'author' to the file above, which makes it easier to compute the h-indices for each author.
 
 * df_h_indices
 <br> This file creates a database of h-indices. This has the form of a dataframe with these columns: 'author', 'year', 'month',
 'yearly_H_index_notincremental', 'yearly_H_index_incremental', 'monthly_H_index_incremental', 'monthly_H_index_notincremental'.
 
 * auxiliarydf_viz
<br> This file creates several databases aiming at measuring the importance of keywords over all the papers.
 