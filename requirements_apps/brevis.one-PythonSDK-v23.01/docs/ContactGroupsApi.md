# swagger_client.ContactGroupsApi

All URIs are relative to *https://10.30.70.20/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**contactgroups_get**](ContactGroupsApi.md#contactgroups_get) | **GET** /contactgroups | Get all contact groups
[**contactgroups_id_contacts_get**](ContactGroupsApi.md#contactgroups_id_contacts_get) | **GET** /contactgroups/{id}/contacts | Get all contacts in the passed contact group
[**contactgroups_id_delete**](ContactGroupsApi.md#contactgroups_id_delete) | **DELETE** /contactgroups/{id} | Delete a contact group by its id
[**contactgroups_id_get**](ContactGroupsApi.md#contactgroups_id_get) | **GET** /contactgroups/{id} | Get a contact group by its id
[**contactgroups_id_post**](ContactGroupsApi.md#contactgroups_id_post) | **POST** /contactgroups/{id} | Update a contact group by its id
[**contactgroups_post**](ContactGroupsApi.md#contactgroups_post) | **POST** /contactgroups | Create a new contact group

# **contactgroups_get**
> list[ContactGroup] contactgroups_get(limit=limit, page=page)

Get all contact groups

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: BasicAuth
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.ContactGroupsApi(swagger_client.ApiClient(configuration))
limit = 10 # int | Limits the number of returned results (optional) (default to 10)
page = 1 # int | The page number of a list of paginated results (optional) (default to 1)

try:
    # Get all contact groups
    api_response = api_instance.contactgroups_get(limit=limit, page=page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContactGroupsApi->contactgroups_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| Limits the number of returned results | [optional] [default to 10]
 **page** | **int**| The page number of a list of paginated results | [optional] [default to 1]

### Return type

[**list[ContactGroup]**](ContactGroup.md)

### Authorization

[BasicAuth](../README.md#BasicAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **contactgroups_id_contacts_get**
> list[Contact] contactgroups_id_contacts_get(id, limit=limit, page=page)

Get all contacts in the passed contact group

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: BasicAuth
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.ContactGroupsApi(swagger_client.ApiClient(configuration))
id = 56 # int | The contact group's id
limit = 10 # int | Limits the number of returned results (optional) (default to 10)
page = 1 # int | The page number of a list of paginated results (optional) (default to 1)

try:
    # Get all contacts in the passed contact group
    api_response = api_instance.contactgroups_id_contacts_get(id, limit=limit, page=page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContactGroupsApi->contactgroups_id_contacts_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| The contact group&#x27;s id | 
 **limit** | **int**| Limits the number of returned results | [optional] [default to 10]
 **page** | **int**| The page number of a list of paginated results | [optional] [default to 1]

### Return type

[**list[Contact]**](Contact.md)

### Authorization

[BasicAuth](../README.md#BasicAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **contactgroups_id_delete**
> contactgroups_id_delete(id)

Delete a contact group by its id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: BasicAuth
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.ContactGroupsApi(swagger_client.ApiClient(configuration))
id = 56 # int | 

try:
    # Delete a contact group by its id
    api_instance.contactgroups_id_delete(id)
except ApiException as e:
    print("Exception when calling ContactGroupsApi->contactgroups_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

[BasicAuth](../README.md#BasicAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **contactgroups_id_get**
> ContactGroup contactgroups_id_get(id)

Get a contact group by its id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: BasicAuth
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.ContactGroupsApi(swagger_client.ApiClient(configuration))
id = 56 # int | 

try:
    # Get a contact group by its id
    api_response = api_instance.contactgroups_id_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContactGroupsApi->contactgroups_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**ContactGroup**](ContactGroup.md)

### Authorization

[BasicAuth](../README.md#BasicAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **contactgroups_id_post**
> ContactGroup contactgroups_id_post(body, id)

Update a contact group by its id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: BasicAuth
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.ContactGroupsApi(swagger_client.ApiClient(configuration))
body = swagger_client.ContactGroupPayload() # ContactGroupPayload | 
id = 56 # int | 

try:
    # Update a contact group by its id
    api_response = api_instance.contactgroups_id_post(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContactGroupsApi->contactgroups_id_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ContactGroupPayload**](ContactGroupPayload.md)|  | 
 **id** | **int**|  | 

### Return type

[**ContactGroup**](ContactGroup.md)

### Authorization

[BasicAuth](../README.md#BasicAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **contactgroups_post**
> ContactGroup contactgroups_post(body)

Create a new contact group

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: BasicAuth
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.ContactGroupsApi(swagger_client.ApiClient(configuration))
body = swagger_client.ContactGroupPayload() # ContactGroupPayload | 

try:
    # Create a new contact group
    api_response = api_instance.contactgroups_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContactGroupsApi->contactgroups_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ContactGroupPayload**](ContactGroupPayload.md)|  | 

### Return type

[**ContactGroup**](ContactGroup.md)

### Authorization

[BasicAuth](../README.md#BasicAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

