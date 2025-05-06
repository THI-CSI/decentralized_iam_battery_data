# Error Handling and Retry Mechanism – Data Transfer

## Overview
This document describes the error handling and retry strategy used for sending data from the client to the cloud.

## Retry Strategy

- Maximum 3 attempts per request
- 2-second wait between retry attempts
- Retry is only triggered for:
  - Network exceptions (e.g. timeout, no response)
  - HTTP 5xx server errors (e.g. 500, 503)

## No-Retry Conditions

- HTTP 4xx client errors (e.g. 400 Bad Request, 401 Unauthorized)
- These indicate issues on the client side and should not be retried

## Location

The logic is implemented in:

```text
cloud/test_client.py

Function used:

send_dummy_data_with_retry(data, max_retries=3)

## Future Improvements

- Use exponential backoff instead of fixed delay  
- Add proper logging of failed attempts  
- Trigger alerts or fallback if all retries fail
