from pandasdmx import Request

# Connecting to the Eurostat web service
estat = Request('ESTAT')

# Downloading the dataflow definitions
flows = estat.dataflow()

# Getting information about the dataflow
flows.url
flows.http_headers

# Exporting the dataflow definitions to a pandas DataFrame
dflows = flows.write().dataflow
# Listing tables from the high tech database and the description of a single table
ht_tabs = dflows[dflows.index.str.startswith('htec') == True]
kia_emp = dflows.loc['htec_kia_emp2'][0]

# Dataflow definition
df_def = flows.dataflow.htec_kia_emp2

# Database's datastructure id
dsd_id = df_def.structure.id

# Creating a support dict
refs = dict(references = 'all')

# Calling the table
dsd_response = estat.get(url = 'http://ec.europa.eu/eurostat/SDMX/diss-web/rest/datastructure/ESTAT/' + dsd_id)

# Getting informatou about the datastructure
dsd_response.url
dsd_response.http_headers

# Getting the datastructure of the table
dsd = dsd_response.datastructure[dsd_id]

# Dimensions and attributes
dsd.measures.aslist()
dsd.dimensions.aslist()
dsd.attributes.aslist()


# Getting dimension values
dsd_response.write().codelist.loc['NACE_R2']

# Getting attribute values
dsd_response.write().codelist.loc['OBS_FLAG']
dsd_response.write().codelist.loc['OBS_STATUS']

# Getting data
estat.get(resource_type = 'data', resource_id = 'htec_kia_emp2', key = {'GEO', 'NACE_R2' : [], 'SEX', 'UNIT'}, params = {'startPeriod': '2016'})
