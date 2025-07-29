import requests
from datetime import datetime
from typing import Union, Literal, List
from mcp.server import FastMCP
from pydantic import Field
from typing import Annotated
from mcp.server.fastmcp import FastMCP
from fastmcp import FastMCP, Context
import os
from dotenv import load_dotenv
load_dotenv()
rapid_api_key = os.getenv("RAPID_API_KEY")

__rapidapi_url__ = 'https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch'

mcp = FastMCP('jsearch')

@mcp.tool()
def job_search(query: Annotated[str, Field(description='Free-form jobs search query. It is highly recommended to include job title and location as part of the query, see query examples below. Examples: web development jobs in chicago marketing manager in new york via linkedin')],
               page: Annotated[Union[int, float, None], Field(description='Page to return (each page includes up to 10 results). Default: 1 Allowed values: 1-100 Default: 1')] = None,
               num_pages: Annotated[Union[int, float, None], Field(description='Number of pages to return, starting from page. Default: 1 Allowed values: 1-20 Note: requests for more than one page and up to 10 pages are charged x2 and requests for more than 10 pages are charged 3x. Default: 1')] = None,
               country: Annotated[Union[str, None], Field(description='Country code of the country from which to return job postings. Please note that this parameter must be set in order to get jobs in a specific country, for example, to query for software developer jobs in Berlin, one should add country=de to the request - e.g. query=software+developers+in+berlin&country=de. Default: us Allowed values: See https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2')] = None,
               language: Annotated[Union[str, None], Field(description='Language code in which to return job postings. Leave empty to use the primary language in the specified country (country parameter). Note that each country supports certain languages. In case a language not supported by the specified country is used, it is likely that no results will be returned. Allowed values: See https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes')] = None,
               date_posted: Annotated[Literal['all', 'today', '3days', 'week', 'month', None], Field(description='Find jobs posted within the time you specify. Default: all Allowed values: all, today, 3days, week, month')] = None,
               work_from_home: Annotated[Union[bool, None], Field(description='Only return work from home / remote jobs. Default: false')] = None,
               employment_types: Annotated[Union[str, None], Field(description='Find jobs of particular employment types, specified as a comma delimited list of the following values: FULLTIME, CONTRACTOR, PARTTIME, INTERN.')] = None,
               job_requirements: Annotated[Union[str, None], Field(description='Find jobs with specific requirements, specified as a comma delimited list of the following values: under_3_years_experience, more_than_3_years_experience, no_experience, no_degree.')] = None,
               radius: Annotated[Union[int, float, None], Field(description='Return jobs within a certain distance from location as specified as part of the query (in km). This internally sent as the Google "lrad" parameter and although it might affect the results, it is not strictly followed by Google for Jobs.')] = None,
               exclude_job_publishers: Annotated[Union[str, None], Field(description='Exclude jobs published by specific publishers, specified as a comma (,) separated list of publishers to exclude. Example: BeeBe,Dice')] = None,
               fields: Annotated[Union[str, None], Field(description='A comma separated list of job fields to include in the response (field projection). By default all fields are returned. Example: employer_name,job_publisher,job_title,job_country')] = None) -> dict: 
    '''Search for jobs posted on any public job site across the web on the largest job aggregate in the world (Google for Jobs). Extensive filtering support and most options available on Google for Jobs.'''
    url = 'https://jsearch.p.rapidapi.com/search'
    headers = {'x-rapidapi-host': 'jsearch.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'query': query,
        'page': page,
        'num_pages': num_pages,
        'country': country,
        'language': language,
        'date_posted': date_posted,
        'work_from_home': work_from_home,
        'employment_types': employment_types,
        'job_requirements': job_requirements,
        'radius': radius,
        'exclude_job_publishers': exclude_job_publishers,
        'fields': fields,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def job_details(job_id: Annotated[str, Field(description='Job Id of the job for which to get details. Batching of up to 20 Job Ids is supported by separating multiple Job Ids by comma (,). Note that each Job Id in a batch request is counted as a request for quota calculation.')],
                country: Annotated[Union[str, None], Field(description='Country code of the country from which to return job posting. Default: us Allowed values: See https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2')] = None,
                language: Annotated[Union[str, None], Field(description='Language code in which to return job postings. Leave empty to use the primary language in the specified country (country parameter). Allowed values: See https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes')] = None,
                fields: Annotated[Union[str, None], Field(description='A comma separated list of job fields to include in the response (field projection). By default all fields are returned. Example: employer_name,job_publisher,job_title,job_country')] = None) -> dict: 
    '''Get all job details, including additional information such as: application options / links, employer reviews and estimated salaries for similar jobs.'''
    url = 'https://jsearch.p.rapidapi.com/job-details'
    headers = {'x-rapidapi-host': 'jsearch.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'job_id': job_id,
        'country': country,
        'language': language,
        'fields': fields,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def job_salary(job_title: Annotated[str, Field(description='Job title for which to get salary estimation.')],
               location: Annotated[str, Field(description='Free-text location/area in which to get salary estimation.')],
               location_type: Annotated[Literal['ANY', 'CITY', 'STATE', 'COUNTRY', None], Field(description='Specify the type of the location you are looking to get salary estimation for additional accuracy. Allowed values: ANY, CITY, STATE, COUNTRY Default: ANY')] = None,
               years_of_experience: Annotated[Literal['ALL', 'LESS_THAN_ONE', 'ONE_TO_THREE', 'FOUR_TO_SIX', 'SEVEN_TO_NINE', 'TEN_TO_FOURTEEN', 'ABOVE_FIFTEEN', None], Field(description='Get job estimation for a specific experience level range (years). Allowed values: ALL, LESS_THAN_ONE, ONE_TO_THREE, FOUR_TO_SIX, SEVEN_TO_NINE, TEN_TO_FOURTEEN, ABOVE_FIFTEEN Default: ALL')] = None,
               fields: Annotated[Union[str, None], Field(description='A comma separated list of job salary fields to include in the response (field projection). By default all fields are returned. Example: job_title,median_salary,location')] = None) -> dict: 
    '''Get estimated salaries / pay for a jobs around a location by job title and location. The salary estimation is returned for several periods, depending on data availability / relevance, and includes: hourly, daily, weekly, monthly, or yearly.'''
    url = 'https://jsearch.p.rapidapi.com/estimated-salary'
    headers = {'x-rapidapi-host': 'jsearch.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'job_title': job_title,
        'location': location,
        'location_type': location_type,
        'years_of_experience': years_of_experience,
        'fields': fields,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def company_job_salary(company: Annotated[str, Field(description='The company name for which to get salary information (e.g. Amazon).')],
                       job_title: Annotated[str, Field(description='Job title for which to get salary estimation.')],
                       location: Annotated[Union[str, None], Field(description='Free-text location/area in which to get salary estimation.')] = None,
                       location_type: Annotated[Literal['ANY', 'CITY', 'STATE', 'COUNTRY', None], Field(description='Specify the type of the location you are looking to get salary estimation for additional accuracy. Allowed values: ANY, CITY, STATE, COUNTRY Default: ANY')] = None,
                       years_of_experience: Annotated[Literal['ALL', 'LESS_THAN_ONE', 'ONE_TO_THREE', 'FOUR_TO_SIX', 'SEVEN_TO_NINE', 'TEN_TO_FOURTEEN', 'ABOVE_FIFTEEN', None], Field(description='Get job estimation for a specific experience level range (years). Allowed values: ALL, LESS_THAN_ONE, ONE_TO_THREE, FOUR_TO_SIX, SEVEN_TO_NINE, TEN_TO_FOURTEEN, ABOVE_FIFTEEN Default: ALL')] = None) -> dict: 
    '''Get estimated job salaries/pay in a specific company by job title and optionally a location and experience level in years.'''
    url = 'https://jsearch.p.rapidapi.com/company-job-salary'
    headers = {'x-rapidapi-host': 'jsearch.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'company': company,
        'job_title': job_title,
        'location': location,
        'location_type': location_type,
        'years_of_experience': years_of_experience,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()



if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9997
    mcp.run(transport="stdio")
