# -*- coding: UTF-8 -*-
# encoding specified for Anaconda per https://www.python.org/dev/peps/pep-0263/ 
# seems to remove need for specifying encoding schema in the with open statement

import csv
import datetime as dt 
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
# from matplotlib.ticker import AutoMinorLocator#, FixedLocator #, MultipleLocator
import pandas as pd 


file_path_relation = "./data/person_to_item.csv"
file_path_person = "./data/person.csv"
file_path_items = "./data/item_refined.csv"

#use pandas to read data for person to item relationship
data_text = pd.read_csv(file_path_relation)

#read data for person list
person_text = pd.read_csv(file_path_person)

#read data for items
item_text = pd.read_csv(file_path_items)


#replace NaNs in data
#see: https://www.codegrepper.com/code-examples/python/replace+nan+in+pandas
person_text['person_fname'].fillna("--", inplace=True) 


#create datafram using just person id and item id
target_df = pd.DataFrame(data_text, columns=['person_id', 'item_id'])


#count the items associated with each person and sort by descending
#this is now a series rather than a dataframe
jobs_per_person = target_df.groupby("person_id")['person_id'].count().sort_values(ascending=False)


person_test_list=[]
# get name for person to item
for identifier, item_number in jobs_per_person.items():
	try:
		#use .loc to get specific information
		#see: https://towardsdatascience.com/8-things-you-should-know-when-dealing-with-pandas-indexes-70835198ac7c
		new_person = person_text['person_id'].loc[identifier-1], person_text['person_fname'].loc[identifier-1], person_text['person_lname'].loc[identifier-1], item_number
		person_test_list.append(new_person)
	except KeyError:
		continue


person_with_count= pd.DataFrame(person_test_list, columns=['person_id', 'person_fname', 'person_lname', 'item_count'])
# print(person_with_count['person_lname'].astype(str).iloc[0:5])

#generate list of top five names for further visualization
top_five_names = list(person_with_count['person_lname'].astype(str).iloc[0:5])
# print(top_five_names)

#join tables to link person and item through person-to-item
#see: https://www.shanelynn.ie/merge-join-dataframes-python-pandas-index-1/
#see also: https://pandas.pydata.org/docs/reference/api/pandas.merge.html
multi_table = pd.merge(data_text, item_text, on='item_id')
multi_table.fillna("--", inplace=True)

#join tables to finish link to item data
multi_table_2 = pd.merge(person_text, multi_table, on='person_id')
# print(multi_table_2.info())

#create dataframe from merged tables
extended_info = pd.DataFrame(multi_table_2, columns=['item_id', 'person_id', 'person_fname', 'person_lname', 'occupation_id', 'gender', 'item_pymnt_amount', 'item_desc_dutch', 'item_desc_translation', 'month_y', 'year_y','manuscript', 'folio_num'])


#output information to csv file for use on website
# csv_header = ['item_id', 'person_id', 'person_fname', 'person_lname', 'item_desc_translation', 'month_y', 'year_y']
# with open('./data/items_by_person.csv', 'a', newline='', encoding='UTF-8') as outbound_csv:
# 		writer = csv.writer(outbound_csv)
# 		writer.writerow(csv_header)

# for row, item in extended_info.iterrows():
# 	new_row = item['item_id'], item['person_id'], item['person_fname'], item['person_lname'], item['item_desc_translation'], item['month_y'], item['year_y']
# 	with open('./data/items_by_person.csv', 'a', newline='', encoding='UTF-8') as outbound_csv:
# 		writer = csv.writer(outbound_csv)
# 		writer.writerow(new_row)
# print("Finished Writing CSV")


#Find and plot top 25 terms
#viz ref: https://datavizpyr.com/bar-plots-with-matplotlib-in-python/

working_stops = []

countable_list = []

def count_search_results(search_results_list):
	'''this function creates a dictionary of terms and counts by using the term as the key and the count as the value.
	If the dictionary does not contain the term, the term is added as a key.
	This approach is found at: https://codeburst.io/python-basics-11-word-count-filter-out-punctuation-dictionary-manipulation-and-sorting-lists-3f6c55420855
	Input: a list of words
	Output: a dictionary of words as keys and counts of those words as values'''
	search_counts_dict = {}
	for term in search_results_list:
		if term not in search_counts_dict:
			search_counts_dict[term] = 0

	for term in search_results_list:
		if term in search_results_list:
			search_counts_dict[term] += 1
	return search_counts_dict

def sort_dict_by_value(d, reverse = True):
	# code from: https://www.w3resource.com/python-exercises/dictionary/python-data-type-dictionary-exercise-1.php
	'''function uses lambda calculus to sort a dictionary. 
	Setting reverse = True arranges information in descending order.
	Input: python dictionary with counts as value for categorical keys.
	Output: sorted dictionary with the option to arrange in ascending or descending order'''
	return dict(sorted(d.items(), key = lambda x: x[1], reverse = reverse))

# # open custom list of stop words for idiosyncratic data
stop_list_file_path = "./data/sorted_stops.txt"

with open (stop_list_file_path, 'r') as inbound_file:
	working_text = inbound_file.read()
	working_stops = working_text


for row, item in extended_info.iterrows():
	working_list = item['item_desc_translation'].split()
	for word in working_list:
		if word not in working_stops:
			new_word = word.replace("(","").replace(")","").strip()
			countable_list.append(new_word)
			# print(word)


#send list to function to make into a dictionary
counted_dict = count_search_results(countable_list)

#send dictionary to function to sort
sorted_dict = sort_dict_by_value(counted_dict)

#separate keys and values for plotting on x, y axes
category = list(sorted_dict.keys())
cat_count = list(sorted_dict.values())


# create plot of word counts using matplotlib and pyplot
# see: https://problemsolvingwithpython.com/06-Plotting-with-Matplotlib/06.13-Plot-Styles/
# see also: https://www.oreilly.com/library/view/python-data-science/9781491912126/ch04.html

caption = 'Total terms: ' + str(len(sorted_dict))

plt.style.use('seaborn-talk')
plt.bar(category[:25], cat_count[:25])
plt.xticks(rotation=60, size=10)
plt.title('Top 25 Terms')
plt.ylabel('Frequency of Terms')
plt.xlabel('Terms')
plt.gcf().subplots_adjust(bottom=0.2)
plt.figtext(0.75, .9, caption, wrap=True, horizontalalignment='center', fontsize=12)

# plt.savefig('./plots/LKP_Top25Terms.png', dpi=300, bbox_inches='tight')

plt.show()

#isolate top n terms for time series plot
terms_to_find = 5
top_n_terms = category[:terms_to_find]


working_terms_list = []
for row, item in extended_info.iterrows():
	for word in item['item_desc_translation'].split():
		if word in top_n_terms:
			#must remove 1405 as an outlier for time series to make sense
			if item['year_y']!= 1405:
				new_row = item['item_id'], word, item['year_y']
				working_terms_list.append(new_row)
			else:
				continue

top_terms_timeseries = pd.DataFrame(working_terms_list, columns=['item_id', 'word', 'year_y'])

#function to get top five terms for plotting
def get_individual_terms(terms_list, target_list, target_num):
	temp_list=[]
	for row, item in terms_list.iterrows():
		if item['word'] == target_list[target_num]:
			# print(item['item_id'], item['word'], item['year_y'])
			# new_row = item['item_id'], item['word'], item['year_y']
			new_row = item
			temp_list.append(new_row)
	return temp_list
			
#NB: if more than 5 terms desired, will need to add lines to proper number of lines (e.g. 8, 10, etc.)
term_0 = pd.DataFrame(get_individual_terms(top_terms_timeseries, top_n_terms, 0), columns=['item_id', 'word', 'year_y'])
term_1 = pd.DataFrame(get_individual_terms(top_terms_timeseries, top_n_terms, 1), columns=['item_id', 'word', 'year_y'])
term_2 = pd.DataFrame(get_individual_terms(top_terms_timeseries, top_n_terms, 2), columns=['item_id', 'word', 'year_y'])
term_3 = pd.DataFrame(get_individual_terms(top_terms_timeseries, top_n_terms, 3), columns=['item_id', 'word', 'year_y'])
term_4 = pd.DataFrame(get_individual_terms(top_terms_timeseries, top_n_terms, 4), columns=['item_id', 'word', 'year_y'])

term_0_word = term_0['word'].iloc[0]
term_1_word = term_1['word'].iloc[0]
term_2_word = term_2['word'].iloc[0]
term_3_word = term_3['word'].iloc[0]
term_4_word = term_4['word'].iloc[0]

term_0_plot = term_0.groupby(['year_y'])['word'].count()
term_1_plot = term_1.groupby(['year_y'])['word'].count()
term_2_plot = term_2.groupby(['year_y'])['word'].count()
term_3_plot = term_3.groupby(['year_y'])['word'].count()
term_4_plot = term_4.groupby(['year_y'])['word'].count()


#plot time series for top n terms
#dates are before 1970 and must use the pandas.Period class. see: https://pandas.pydata.org/docs/reference/api/pandas.Period.html
#value = period represented, frequency = string rep of how to subdivide the period (e.g. day, week, month, etc.)
start_date = pd.Period(value='1452', freq='M', year=1452, month=6, day=1)
end_date = pd.Period(value='1464', freq='M', year=1464, month=6, day=1)
date_range = pd.period_range(start_date, end_date)

plt.figure(figsize=[11,8])
plt.plot(plt = plt, x_compat=True) #seems to help the plot recognize the xaxis later
plt.style.use('seaborn-muted')
#color list: https://matplotlib.org/3.1.0/gallery/color/named_colors.html
plt.plot(term_0_plot, color='dimgray', marker='o', markersize='5')
plt.plot(term_1_plot, color='goldenrod', marker='o', markersize='5')
plt.plot(term_2_plot, color='forestgreen', marker='o', markersize='5')
plt.plot(term_3_plot, color='mediumblue', marker='o', markersize='5')
plt.plot(term_4_plot, color='maroon', marker='o', markersize='5')


plt.title('Count Per Year For Top 5 Terms')
plt.xlabel('Year')
plt.ylabel('Term Count')
plt.gcf().subplots_adjust(bottom=0.15)
# plt.xticks(date_range.year)
plt.xticks(size=6)
plt.yticks(size=6)

#create legend, see: https://matplotlib.org/1.3.1/users/legend_guide.html
red_line = mlines.Line2D([], [], color='dimgray', markersize=4, label=term_0_word)
blue_line = mlines.Line2D([], [], color='goldenrod', markersize=4, label=term_1_word)
green_line = mlines.Line2D([], [], color='forestgreen', markersize=4, label=term_2_word)
darkorange_line = mlines.Line2D([], [], color='mediumblue', markersize=4, label=term_3_word)
purple_line = mlines.Line2D([], [], color='maroon', markersize=4, label=term_4_word)

plt.legend(handles=[red_line, blue_line, green_line, darkorange_line, purple_line])       

# plt.savefig('./plots/LKP_TimeSeries_1.png', dpi=300, bbox_inches='tight')

plt.show()


# #Create Dataframe and plot time series for top 5 names
top_five_viz_data_list = []

for row, item in extended_info.iterrows():
	if (item['person_lname'] in top_five_names):
		#Convert string months to int months
		#see: https://www.kite.com/python/answers/how-to-convert-between-month-name-and-month-number-in-python
		temp_month = dt.datetime.strptime(item['month_y'], '%B').month
		temp_entry = item['item_id'], item['person_id'], item['person_fname'], item['person_lname'], item['item_pymnt_amount'], item['item_desc_translation'], temp_month, item['year_y']
		top_five_viz_data_list.append(temp_entry)
		
	else:
		continue

#create function to get individuals from top five list groped by person_id
def get_individual_groups(person_list, group_list, target_num):
	temp_list=[]
	for item in person_list:
		if item[3] == group_list[target_num]:
			temp_list.append(item)
	return temp_list


#create individual data frames for top five individuals for plotting
person_0 = pd.DataFrame(get_individual_groups(top_five_viz_data_list, top_five_names, 0), columns=['item_id', 'person_id', 'person_fname', 'person_lname','item_pymnt_amount', 'item_desc_translation', 'month_y', 'year_y'])
person_1 = pd.DataFrame(get_individual_groups(top_five_viz_data_list, top_five_names, 1), columns=['item_id', 'person_id', 'person_fname', 'person_lname','item_pymnt_amount', 'item_desc_translation', 'month_y', 'year_y'])
person_2 = pd.DataFrame(get_individual_groups(top_five_viz_data_list, top_five_names, 2), columns=['item_id', 'person_id', 'person_fname', 'person_lname','item_pymnt_amount', 'item_desc_translation', 'month_y', 'year_y'])
person_3 = pd.DataFrame(get_individual_groups(top_five_viz_data_list, top_five_names, 3), columns=['item_id', 'person_id', 'person_fname', 'person_lname','item_pymnt_amount', 'item_desc_translation', 'month_y', 'year_y'])
person_4 = pd.DataFrame(get_individual_groups(top_five_viz_data_list, top_five_names, 4), columns=['item_id', 'person_id', 'person_fname', 'person_lname','item_pymnt_amount', 'item_desc_translation', 'month_y', 'year_y'])


# group items by year and plot for each
person_0_plot = person_0.groupby(['year_y'])['item_id'].count()
person_1_plot = person_1.groupby(['year_y'])['item_id'].count()
person_2_plot = person_2.groupby(['year_y'])['item_id'].count()
person_3_plot = person_3.groupby(['year_y'])['item_id'].count()
person_4_plot = person_4.groupby(['year_y'])['item_id'].count()


#isolate name for person
person_0_name = person_0['person_fname'][0] +  " " + person_0['person_lname'][0]
person_1_name = person_1['person_fname'][0] +  " " + person_1['person_lname'][0]
person_2_name = person_2['person_fname'][0] +  " " + person_2['person_lname'][0]
person_3_name = person_3['person_fname'][0] +  " " + person_3['person_lname'][0]
person_4_name = person_4['person_fname'][0] +  " " + person_4['person_lname'][0]

#plot time series from top 5 names data

plt.figure(figsize=[11,8])
plt.plot(plt = plt, x_compat=True) #seems to help the plot recognize the xaxis later
plt.style.use('seaborn-muted')
plt.plot(person_0_plot, color='red', marker='o', markersize='5')
plt.plot(person_1_plot, color='blue', marker='o', markersize='5')
plt.plot(person_2_plot, color='green', marker='o', markersize='5')
plt.plot(person_3_plot, color='darkorange', marker='o', markersize='5')
plt.plot(person_4_plot, color='purple', marker='o', markersize='5')


plt.title('Items Per Year For Top 5 Names')
plt.xlabel('Year')
plt.ylabel('Item Count')
plt.gcf().subplots_adjust(bottom=0.15)
plt.xticks(date_range.year)
plt.xticks(size=6)
plt.yticks(size=6)

#possibly try to add a minor tick for months? See: https://matplotlib.org/3.1.1/gallery/ticks_and_spines/tick-locators.html
# plt.gca().xaxis.get_minor_locator() 
# plt.gca().xaxis.set_minor_locator(AutoMinorLocator(date_range.strptime('%m')))

#create legend, see: https://matplotlib.org/1.3.1/users/legend_guide.html
red_line = mlines.Line2D([], [], color='red', markersize=4, label=person_0_name)
blue_line = mlines.Line2D([], [], color='blue', markersize=4, label=person_1_name)
green_line = mlines.Line2D([], [], color='green', markersize=4, label=person_2_name)
darkorange_line = mlines.Line2D([], [], color='darkorange', markersize=4, label=person_3_name)
purple_line = mlines.Line2D([], [], color='purple', markersize=4, label=person_4_name)

plt.legend(handles=[red_line, blue_line, green_line, darkorange_line, purple_line])       

# plt.savefig('./plots/LKP_TimeSeries_2.png', dpi=300, bbox_inches='tight')

plt.show()


#plot to 30 names data from dataframe
caption_1 = "Total number of entries:", data_text.shape[0] #see: https://www.codegrepper.com/code-examples/python/pandas+get+length+of+dataframe
caption_2 ="Total number of names mentioned:", person_text.shape[0]

x_axis=person_with_count['person_lname'].astype(str).iloc[0:30]
y_axis=person_with_count['item_count'].iloc[0:30]

plt.figure(figsize=[11,8])
plt.style.use('seaborn-talk')
# plt.bar(x_axis, y_axis)
plt.barh(x_axis, y_axis)
plt.gca().invert_yaxis()
plt.gcf().subplots_adjust(left=0.3)
plt.xticks(size=6)
plt.yticks(size=6)
plt.title('30 Most Mentioned Names')
plt.xlabel('Number of Items Associated with Name')
plt.ylabel('Person Last Name')
plt.figtext(0.75, .6, caption_1, wrap=True, horizontalalignment='center', fontsize=8)
plt.figtext(0.75, .57, caption_2, wrap=True, horizontalalignment='center', fontsize=8)

# plt.savefig('./plots/LKP_Top30Names_1.png', dpi=300, bbox_inches='tight')

plt.show()




