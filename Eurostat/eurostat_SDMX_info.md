# Eurostat SDMX

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

## Information about REST query building:
* http://ec.europa.eu/eurostat/web/sdmx-web-services/rest-sdmx-2.1
* http://sdmx.org/wp-content/uploads/SDMX_2-1-1-SECTION_07_WebServicesGuidelines_2013-04.pdf

## Useful tips for using the REST api
* https://github.com/sdmx-twg/sdmx-rest/wiki/Tips-for-consumers


## REST query structure
### REST SDMX 2.1 format
* http://ec.europa.eu/SDMX/diss-web/rest/resource/agencyID/resourceID/version

### List of available datasets
* http://ec.europa.eu/eurostat/SDMX/diss-web/rest/dataflow/ESTAT/all/latest

## Querying data
The following examples show the structure of the queries
http://ec.europa.eu/eurostat/SDMX/diss-web/rest/resource/flowRef/key/providerRef
OR
http://ec.europa.eu/eurostat/SDMX/diss-web/rest/resource/flowRef/key[?[startPeriod=yyyy[mmdd]&]endPeriod=yyyy[mmdd]]

> The response is provided by default in SDMX-ML 2.1 generic schema. Modify the HTTP header field `Accept` with `application/vnd.sdmx.structurespecificdata+xml` to receive a response in SDMX-ML 2.1 structure specific schema.
> Further information: https://sdmx.org/wp-content/uploads/SDMX_2-1-1-SECTION_07_WebServicesGuidelines_2013-04.pdf

### Elements
1. **resource** is the desired resource or artifact (in this case we want to retrieve data, so it would be "data"),
2. **flowRef** is the reference to the dataflow (e.g. nama_gdp_c), and
3. **key** is the set of filters to be applied, plus
4. **?[startPeriod=yyyy[mmdd]&]endPeriod=yyyy[mmdd]** for any optional additional time filtering. The Date format could contain only the year or the year and the month or, the detailed information, year, month and day.

### Examples
For instance , the request below demands
* the data of cdh_e_fos
* for all frequencies (FREQ) and year of graduation (Y_GRAD),
* UNIT=PC (percentage)
* FOS7(Field of Science)=FOS1(Natural Sciences)
* GEO=BE(Belgium)
* from 2005 to 2011

> http://ec.europa.eu/eurostat/SDMX/diss-web/rest/data/cdh_e_fos/..PC.FOS1.BE/?startperiod=2005&endPeriod=2011


> #### Further information
> http://sdmx.org/wp-content/uploads/SDMX_2-1-1-SECTION_07_WebServicesGuidelines_2013-04.pdf

## Query steps
### 1. Identify dataflow

List of available dataflows: http://ec.europa.eu/eurostat/SDMX/diss-web/rest/dataflow/ESTAT/all/latest

### 2. Check the dimensions and their elements.

By retrieving the Data Structure Definition (DSD), e.g. the REST request for the DSD about nama_gdp_c is http://ec.europa.eu/eurostat/SDMX/diss-web/rest/datastructure/ESTAT/DSD_nama_gdp_c

## pandas DataReader
DataReader supports Eurostat access: https://pandas-datareader.readthedocs.io/en/latest/remote_data.html#eurostat

### Basic use
```python
import pandas_datareader.data as web

# Aiming the following target url: http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=tran_sf_railac&lang=en
df = web.DataReader("tran_sf_railac", 'eurostat')
```
### Caching queries
`pandas-datareader` allows you to cache queries using `requests_cache` by passing a `requests_cache.Session` to `DataReader` or `Options` using the session parameter.

```python
import pandas_datareader.data as web
```

## pandaSDMX
Use pandaSDMX: https://pandasdmx.readthedocs.io/en/latest/

### Writing large datasets to pandas DataFrames is slow
* In case of regular data such as monthly (not trading day!), call the write method with `fromfreq` set to `True` so that only the first string will be parsed and the rest inferred from the frequency of the series.
* If the series is stored in the XML document in reverse chronological order, the `reverse_ob`s argument must be set to `True` as well to prevent the resulting dataframe index from extending into a remote future

Eurostat does not support category schemes!!

### Using Request()
```python
from pandasdmx import Request as rq

# Connecting to the Eurostat web service
estat = rq('ESTAT')

# Downloading the dataflow definitions
flows = estat.dataflow()
```

### Using get and msg
```python
from pandasdmx import Request as rq

# Connecting the Eurostat service
estat = rq('ESTAT')

# Using the `get` method
cat_rsp = estat.get(resource_type = 'dataflow')

# Using the 'msg' method
cat_msg = cat_rsp.msg

# Taking name end description
df = cat_rsp.write(columns = ['name', 'description']).dataflow
```

## Generic or structure-specific data
### Generic
Self-contained, but not memory efficient, usable for smaller data sets.
### Structure-specific
Memory efficient, but requires datastructure definition (DSD) to interpret the XML.

The response is provided by default in **SDMX-ML 2.1 generic schema**. Modify the HTTP request header field _Accept: application/vnd.sdmx.structurespecificdata+xml_ to receive a response in **SDMX-ML 2.1 structure specific** schema.

### Possible headers
#### General data
```
application/vnd.sdmx.genericdata+xml;version=2.1
application/vnd.sdmx.structurespecificdata+xml;version=2.1
```

#### Time series data
```
application/vnd.sdmx.generictimeseriesdata+xml;version=2.1
application/vnd.sdmx.structurespecifictimeseriesdata+xml;version=2.1
```

#### Metadata
```
application/vnd.sdmx.genericmetadata+xml;version=2.1
application/vnd.sdmx.structurespecificmetadata+xml;version=2.1
```

#### Structure/schema
```
application/vnd.sdmx.structure+xml;version=2.1
application/vnd.sdmx.schema+xml;version=2.1
```

## Filtering

```python
data_response = estat.get(resource_id = 'EXR', key={'CURRENCY': ['USD', 'JPY']}, params = {'startPeriod': '2016'})
```
