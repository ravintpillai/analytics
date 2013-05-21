import Object_Oriented_Analytics_2 as OOA2

my_query = OOA2.Query(OOA2.get_query_type())
results = my_query.get_results()

def print_results(result_dict,query_object):
    results_file = open(filename,'w+')
    results_as_string = ''
    aDimensionList = query_object.get_dimensions().split(',')
    if not aDimensionList[0]:
        aDimensionList = []
    aMetricList = query_object.get_metrics().split(',')
    try:
        for lists in result_dict['rows']:
            for number in range(len(aDimensionList),len(lists)):
                results_as_string += lists[number]+'\t'
                results_file.write(lists[number]+'\t')
        results_file.write('\n')
    except:
        pass
    results_file.close()

def print_all_results(results,query_object):
    for results_dictionary in results:
        print_results(results_dictionary,query_object)

def summarize_all_results(results_list):
    for result in results_list:
        OOA2.result_summarize(result)

def site_segment_date(result_number):
    return (results[result_number]['profileInfo']['profileName'],results[result_number]['query']['segment'],results[result_number]['query']['start-date'],results[result_number]['query']['end-date'])

def get_number_of_dimensions(query_object):
    aDimensionList = query_object.get_dimensions().split(',')
    if aDimensionList[0] != '':
        number_of_dims = len(aDimensionList)
    else:
        number_of_dims = 0
    return number_of_dims

def get_number_of_metrics(query_object):
    aMetricList = query_object.get_metrics().split(',')
    if aMetricList[9] != '':
        number_of_mets = len(aMetricList)
    else:
        number_of_mets = 0
    return number_of_mets

def map_dims_and_mets_to_results(query_object,result_number):
    dim_num = get_number_of_dimensions(query_object)
    mapping = {}
    try:
        results[result_number]['rows']
        for things in results[result_number]['rows']:
            mapping[tuple(things[:dim_num])] = things[dim_num:]
    except:
        pass
    return mapping

def create_mapping():
    super_mapping = {}
    for set_of_results in range(len(results)):
        super_mapping[site_segment_date(set_of_results)] = map_dims_and_mets_to_results(my_query,set_of_results)
    return super_mapping

def result_parameters_set(mapping):
    return mapping.keys()

def unique_segment_date_combos(mapping):
    seg_date_combo = []
    for x in mapping.keys():
            if x[1:] not in seg_date_combo:
                    seg_date_combo.append(x[1:])
            else:
                    pass
    return seg_date_combo

def grouping_mapping(unique_combo,mapping):
	group = []
	for keys in mapping:
		if keys[1:] == unique_combo:
			group.append((keys,mapping[keys]))
	return group

def create_groups(unique_segment_date_combos,mapping):
    uber_group = []
    for combo in unique_segment_date_combos:
        uber_group.append(grouping_mapping(combo,mapping))
    return uber_group

def print_grouped(grouped):
    for x in grouped:
        print x,'\n\n\n'

def get_dimension_sets_of_group(group):
    dimensions_of_group = []
    for dims in group:
        for dim_groups in dims[1].keys():
            if dim_groups not in dimensions_of_group:
                dimensions_of_group.append(dim_groups)
    return dimensions_of_group


def get_metric_sets_of_group(group):
    return OOA2.my_query.get_metrics()
    
    
#filename = OOA2.ca.getFilename()
mapping = create_mapping()
segment_ids_to_segment_names = {v:k for k,v in OOA2.gw.si.segments_Dictionary.items()}
unique_segment_date_combos = unique_segment_date_combos(mapping)
grouped = create_groups(unique_segment_date_combos,mapping)
print_grouped(grouped)
#print_all_results(results,my_query)


