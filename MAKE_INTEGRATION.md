# Make.com Integration Guide for Techline Custom Agent

## Overview
This guide shows how to integrate your GCP-deployed Techline Custom Agent with Make.com scenarios.

## GCP Deployment URLs
After deploying to Cloud Run, your API will be available at:
```
https://techline-custom-agent-[hash]-uc.a.run.app
```

## Make.com HTTP Module Configuration

### 1. Start Conversation
**Module**: HTTP - Make a Request
- **URL**: `https://your-cloud-run-url.app/start_conversation`
- **Method**: POST
- **Headers**: 
  - `Content-Type`: `application/json`
- **Body**: (empty)

**Response**: 
```json
{
  "thread_id": "thread_xyz123",
  "message": "Hello! Welcome to Techline...",
  "requires_address": true
}
```

### 2. Validate Address
**Module**: HTTP - Make a Request
- **URL**: `https://your-cloud-run-url.app/validate_address`
- **Method**: POST
- **Headers**: 
  - `Content-Type`: `application/json`
- **Body**: 
```json
{
  "address": "{{user_address}}",
  "thread_id": "{{thread_id_from_step_1}}"
}
```

### 3. Chat with Assistant (after validation)
**Module**: HTTP - Make a Request
- **URL**: `https://your-cloud-run-url.app/chat`
- **Method**: POST
- **Headers**: 
  - `Content-Type`: `application/json`
- **Body**: 
```json
{
  "message": "{{user_message}}",
  "thread_id": "{{thread_id_from_step_1}}"
}
```

### 4. Get Conversation History
**Module**: HTTP - Make a Request
- **URL**: `https://your-cloud-run-url.app/get_conversation/{{thread_id}}`
- **Method**: GET
- **Headers**: 
  - `Content-Type`: `application/json`

## Example Make.com Scenario Flow

1. **Webhook/Trigger** → Receives user input
2. **HTTP Module** → Start conversation (get thread_id)
3. **HTTP Module** → Validate address
4. **Router** → Check if address is valid
   - **Valid**: Continue to chat
   - **Invalid**: Send error message
5. **HTTP Module** → Chat with assistant
6. **HTTP Module** → Get full conversation for logging/CRM
7. **Response/Action** → Send result back to user

## Error Handling in Make.com

### Common Error Responses:
- **400**: Bad request (missing thread_id, invalid data)
- **404**: Thread not found
- **500**: Server error

### Make.com Error Handling:
1. Add **Error Handler** modules after each HTTP request
2. Check HTTP status code
3. Parse error messages from response body
4. Implement retry logic for temporary failures

## Environment Variables for GCP

Set these in Cloud Run:
```
OPENAI_API_KEY=your_openai_key
GOOGLE_MAPS_API_KEY=your_google_maps_key
PORT=8080
```

Or use Secret Manager for better security.

## Testing Your Integration

Use the test script provided:
```bash
python test_api.py
```

Replace `localhost:8000` with your Cloud Run URL in the test script.

## Production Considerations

1. **Rate Limiting**: Consider implementing rate limiting for Make.com requests
2. **Authentication**: Add API key authentication if needed
3. **Logging**: Implement proper logging for debugging Make.com integration
4. **Monitoring**: Set up Cloud Monitoring for your Cloud Run service
5. **Database**: Replace in-memory thread storage with Cloud Firestore or Cloud SQL
