import json
import asyncio
import time
import statistics
import pytest
from httpx import AsyncClient

API_URL = "http://localhost:1313/predict"  # Update with your actual API endpoint


@pytest.mark.asyncio
async def test_performance():
    # Prepare sample data for testing
    with open('output_4.json', 'r') as f:
        sample_data = json.load(f)

    # Number of requests to simulate
    num_requests = 1000

    # List to store response times
    response_times = []

    # Create a list of tasks for concurrent API requests
    tasks = [make_api_request(sample_data, response_times) for _ in range(num_requests)]

    # Execute tasks concurrently
    await asyncio.gather(*tasks)

    # Calculate and print performance metrics
    print(f"Minimum response time: {min(response_times):.6f} seconds")
    print(f"Maximum response time: {max(response_times):.6f} seconds")
    print(f"Average response time: {statistics.mean(response_times):.6f} seconds")
    print(f"Total number of requests: {num_requests}")


async def make_api_request(data, response_times):
    async with AsyncClient() as client:
        # Record the start time
        start_time = time.time()

        # Make a POST request to the API endpoint
        response = await client.post(API_URL, json=data)

        # Record the end time
        end_time = time.time()

        # Calculate the response time
        response_time = end_time - start_time

        # Append the response time to the list
        response_times.append(response_time)

        return response