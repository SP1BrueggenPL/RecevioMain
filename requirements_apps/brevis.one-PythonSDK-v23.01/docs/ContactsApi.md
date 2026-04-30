# swagger_client.ContactsApi

All URIs are relative to *https://10.30.70.20/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**contacts_get**](ContactsApi.md#contacts_get) | **GET** /contacts | Get all contacts
[**contacts_id_delete**](ContactsApi.md#contacts_id_delete) | **DELETE** /contacts/{id} | Delete a contact by its id
[**contacts_id_get**](ContactsApi.md#contacts_id_get) | **GET** /contacts/{id} | Get a contact by its id
[**contacts_id_post**](ContactsApi.md#contacts_id_post) | **POST** /contacts/{id} | Update a contact by its id
[**contacts_post**](ContactsApi.md#contacts_post) | **POST** /contacts | Create a new contact

# **contacts_get**
> list[Contact] contacts_get(group=group, limit=limit, page=page)

Get all contacts

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
api_instance = swagger_client.ContactsApi(swagger_client.ApiClient(configuration))
group = [56] # list[int] | A comma separated string of group ids or names to filter by (optional)
limit = 10 # int | Limits the number of returned results (optional) (default to 10)
page = 1 # int | The page number of a list of paginated results (optional) (default to 1)

try:
    # Get all contacts
    api_response = api_instance.contacts_get(group=group, limit=limit, page=page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContactsApi->contacts_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group** | [**list[int]**](int.md)| A comma separated string of group ids or names to filter by | [optional] 
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

# **contacts_id_delete**
> contacts_id_delete(id)

Delete a contact by its id

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
api_instance = swagger_client.ContactsApi(swagger_client.ApiClient(configuration))
id = 56 # int | 

try:
    # Delete a contact by its id
    api_instance.contacts_id_delete(id)
except ApiException as e:
    print("Exception when calling ContactsApi->contacts_id_delete: %s\n" % e)
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

# **contacts_id_get**
> Contact contacts_id_get(id)

Get a contact by its id

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
api_instance = swagger_client.ContactsApi(swagger_client.ApiClient(configuration))
id = 56 # int | 

try:
    # Get a contact by its id
    api_response = api_instance.contacts_id_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContactsApi->contacts_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**|  | 

### Return type

[**Contact**](Contact.md)

### Authorization

[BasicAuth](../README.md#BasicAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **contacts_id_post**
> Contact contacts_id_post(body, id)

Update a contact by its id

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
api_instance = swagger_client.ContactsApi(swagger_client.ApiClient(configuration))
body = swagger_client.ContactPayload() # ContactPayload | 
id = 56 # int | 

try:
    # Update a contact by its id
    api_response = api_instance.contacts_id_post(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContactsApi->contacts_id_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ContactPayload**](ContactPayload.md)|  | 
 **id** | **int**|  | 

### Return type

[**Contact**](Contact.md)

### Authorization

[BasicAuth](../README.md#BasicAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **contacts_post**
> Contact contacts_post(body)

Create a new contact

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
api_instance = swagger_client.ContactsApi(swagger_client.ApiClient(configuration))
body = swagger_client.ContactPayload() # ContactPayload | 

try:
    # Create a new contact
    api_response = api_instance.contacts_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContactsApi->contacts_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ContactPayload**](ContactPayload.md)|  | 

### Return type

[**Contact**](Contact.md)

### Authorization

[BasicAuth](../README.md#BasicAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

