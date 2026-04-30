# swagger_client.MessagesApi

All URIs are relative to *https://10.30.70.20/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**messages_get**](MessagesApi.md#messages_get) | **GET** /messages | Get messages from the server
[**messages_id_delete**](MessagesApi.md#messages_id_delete) | **DELETE** /messages/{id} | Delete a message by its id
[**messages_id_get**](MessagesApi.md#messages_id_get) | **GET** /messages/{id} | Get a message by its id
[**messages_post**](MessagesApi.md#messages_post) | **POST** /messages | Send a message using one of the supported providers

# **messages_get**
> list[Message] messages_get(type=type, provider=provider, number=number, user=user, start_date=start_date, end_date=end_date)

Get messages from the server

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
api_instance = swagger_client.MessagesApi(swagger_client.ApiClient(configuration))
type = ['type_example'] # list[str] | A comma separated string of message status:   <br><br>1. `sent :` for sent messages       <br>2. `failed:` for failed messages       <br>3. `queued:` for messages which are queued to be sent       <br>4. `incoming (Default):` for incoming/received messages  (optional)
provider = ['provider_example'] # list[str] | A comma separated list of message providers:   <br><br>1. `sms:` Messages sent/received using sms provider        <br>2. `telegram:` Messages sent/received using telegram provider       <br><br> When this query is omitted then both sms & telegram will be used  (optional)
number = 'number_example' # str | The phone number which sent/received the message (optional)
user = 'user_example' # str | The system's username or id who sent the message (optional)
start_date = 'start_date_example' # str | The start date (optional)
end_date = 'end_date_example' # str | The end date (optional)

try:
    # Get messages from the server
    api_response = api_instance.messages_get(type=type, provider=provider, number=number, user=user, start_date=start_date, end_date=end_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MessagesApi->messages_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **type** | [**list[str]**](str.md)| A comma separated string of message status:   &lt;br&gt;&lt;br&gt;1. &#x60;sent :&#x60; for sent messages       &lt;br&gt;2. &#x60;failed:&#x60; for failed messages       &lt;br&gt;3. &#x60;queued:&#x60; for messages which are queued to be sent       &lt;br&gt;4. &#x60;incoming (Default):&#x60; for incoming/received messages  | [optional] 
 **provider** | [**list[str]**](str.md)| A comma separated list of message providers:   &lt;br&gt;&lt;br&gt;1. &#x60;sms:&#x60; Messages sent/received using sms provider        &lt;br&gt;2. &#x60;telegram:&#x60; Messages sent/received using telegram provider       &lt;br&gt;&lt;br&gt; When this query is omitted then both sms &amp; telegram will be used  | [optional] 
 **number** | **str**| The phone number which sent/received the message | [optional] 
 **user** | **str**| The system&#x27;s username or id who sent the message | [optional] 
 **start_date** | **str**| The start date | [optional] 
 **end_date** | **str**| The end date | [optional] 

### Return type

[**list[Message]**](Message.md)

### Authorization

[BasicAuth](../README.md#BasicAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **messages_id_delete**
> messages_id_delete(id)

Delete a message by its id

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
api_instance = swagger_client.MessagesApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Delete a message by its id
    api_instance.messages_id_delete(id)
except ApiException as e:
    print("Exception when calling MessagesApi->messages_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[BasicAuth](../README.md#BasicAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **messages_id_get**
> Message messages_id_get(id)

Get a message by its id

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
api_instance = swagger_client.MessagesApi(swagger_client.ApiClient(configuration))
id = 'id_example' # str | 

try:
    # Get a message by its id
    api_response = api_instance.messages_id_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MessagesApi->messages_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**Message**](Message.md)

### Authorization

[BasicAuth](../README.md#BasicAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **messages_post**
> list[Message] messages_post(body)

Send a message using one of the supported providers

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
api_instance = swagger_client.MessagesApi(swagger_client.ApiClient(configuration))
body = swagger_client.MessagePayload() # MessagePayload | 

try:
    # Send a message using one of the supported providers
    api_response = api_instance.messages_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MessagesApi->messages_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**MessagePayload**](MessagePayload.md)|  | 

### Return type

[**list[Message]**](Message.md)

### Authorization

[BasicAuth](../README.md#BasicAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

