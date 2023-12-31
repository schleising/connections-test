import time
import asyncio

import requests
import aiohttp

from rich.progress import track, Progress

def requests_no_session(requests_to_make: int) -> None:
    # Start a timer
    start = time.perf_counter()

    # Make the requests
    for _ in track(range(requests_to_make), description='Making requests'):
        response = requests.get('https://schleising.net/football/api/')

        # Check the status code
        if response.status_code != 200:
            print('Error!')
            break

    # Stop the timer
    end = time.perf_counter()

    # Print the time
    print(f'Requests without Session Took: {end - start:.2f}s')

def requests_with_session(requests_to_make: int) -> None:
    # Start a timer
    start = time.perf_counter()

    with requests.session() as session:
        # Make the requests
        for _ in track(range(requests_to_make), description='Making requests'):
            response = session.get('https://schleising.net/football/api/')

            # Check the status code
            if response.status_code != 200:
                print('Error!')
                break

    # Stop the timer
    end = time.perf_counter()

    # Print the time
    print(f'Requests with Session Took   : {end - start:.2f}s')

async def aiohttp_make_request(session: aiohttp.ClientSession) -> None:
    async with session.get('https://schleising.net/football/api/') as response:
        # Check the status code
        if response.status != 200:
            print('Error!')
        else:
            await response.text()

async def aiohttp_with_session(requests_to_make: int) -> None:
    # Start a timer
    start = time.perf_counter()

    # Create a progress bar
    with Progress() as progress:
        task_id = progress.add_task('Making requests', total=requests_to_make)

        # Create a session
        async with aiohttp.ClientSession() as session:
            # Create a task group
            async with asyncio.TaskGroup() as task_group:
                # Create the tasks
                tasks = [task_group.create_task(aiohttp_make_request(session)) for _ in range(requests_to_make)]

                # Add a done callback to the task group to update the progress bar
                for task in tasks:
                    task.add_done_callback(lambda _: progress.advance(task_id))

    # Stop the timer
    end = time.perf_counter()

    # Print the time
    print(f'aiohttp with Session Took    : {end - start:.2f}s')

if __name__ == '__main__':
    # Set the number of requests to make
    requests_to_make = 1000

    # Make 1000 requests without a session
    requests_no_session(requests_to_make)

    # Make 1000 requests with a session
    requests_with_session(requests_to_make)

    # Make 1000 requests with aiohttp
    asyncio.run(aiohttp_with_session(requests_to_make))
