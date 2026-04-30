# Message

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The message&#x27;s id | [optional] 
**type** | **str** | The type / status of the message:   &lt;br&gt;&lt;br&gt;1. &#x60;sent :&#x60; The message is sent       &lt;br&gt;2. &#x60;failed:&#x60; The message failed to be sent       &lt;br&gt;3. &#x60;queued:&#x60; The message is in the \&quot;to be sent\&quot; queue       &lt;br&gt;4. &#x60;incoming:&#x60; The message is received  | [optional] 
**text** | **str** | The message&#x27;s text | [optional] 
**provider** | **str** | The message&#x27;s provider:   &lt;br&gt;&lt;br&gt;1. &#x60;sms :&#x60; The message is a sms message       &lt;br&gt;2. &#x60;telegram:&#x60; The message is a telegram message  | [optional] 
**timestamp** | **str** | The message&#x27;s timestamp | [optional] 
**is_flash** | **bool** | True when the message is a flash message | [optional] 
**is_ring** | **bool** | True when the message is a ring message | [optional] 
**senders** | [**list[Contact]**](Contact.md) |  | [optional] 
**recipients** | [**list[Contact]**](Contact.md) | The contact entries of the message | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

