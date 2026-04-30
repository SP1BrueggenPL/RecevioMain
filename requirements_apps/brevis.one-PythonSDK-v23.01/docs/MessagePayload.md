# MessagePayload

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**recipients** | [**list[MessagePayloadRecipients]**](MessagePayloadRecipients.md) | An array of recipients | 
**text** | **str** | Content of the text message | 
**provider** | **str** | The name of the provider | [optional] [default to 'sms']
**type** | **str** | Describes the type of the message: &lt;br&gt;&lt;br&gt; 1. &#x60;default: &#x60; Use the default configured type&lt;br&gt;&lt;br&gt; 2. &#x60;flash:&#x60; &lt;b&gt;&#x60;ONLY WHEN THE SMS PROVIDER IS USED&#x60;&lt;b&gt; When true, the message appears directly on the recipient&#x27;s phone display and it is not stored when dismissed. Most phones support this feature, but not all. Flash messages are useful during emergency situations &lt;br&gt;&lt;br&gt; 3. &#x60;ring:&#x60; &lt;b&gt;&#x60;ONLY WHEN THE SMS PROVIDER IS USED&#x60;&lt;b&gt; When true then instead of sending an SMS, a voice call will be made to the recipient&#x27;s phone number but when the recipient picks up the call nothing will be heard. Note that voice calls might not be supported by your unit&#x27;s modem. Ring messages are useful during emergency situations.&lt;br&gt;  Note that even if you choose the &#x60;ring&#x60; type you will need to provide a text with at least one character.  | [optional] [default to 'default']

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

