# UmaMusumeAPI

UmaMusumeAPI is an unofficial, asynchronous Python API wrapper designed to extract game data from gametora's [Umamusume](https://gametora.com/umamusume) website. 

Built with modern Python features, it utilizes `aiohttp` for asynchronous web requests and `pydantic` to provide robust, statically typed data models for all extracted game information.

## Key Features

- **Fully Asynchronous**: Uses `aiohttp` to perform non-blocking requests, making it fast and efficient.
- **Built-in Caching**: Integrated with `aiohttp-client-cache` (using a SQLite backend) to minimize redundant network requests and improve response times.
- **Typed Data Models**: Implements extensive `pydantic` models for strong typing, data validation, and IDE autocompletion support. Includes detailed schemas for:
  - Characters (Basic and Detailed)
  - Support Cards and Support Effects
  - Skills
  - Races and Racetracks
  - Scenarios
  - Status Effects
  
  *(Note: The data models do not capture all available information in the database; they have been intentionally designed to include only the most pertinent and commonly used information.)*
- **Easy to Use**: Designed as an async context manager for clean and safe session lifecycle management.

## Installation

Ensure you have Python 3.10+ installed. This project uses `Pipenv` for dependency management. 

To set up the environment locally, clone the repository and run:

```bash
pipenv install
```

## Quick Start

Here is a simple example of how to fetch character data using the API:

```python
import asyncio
from umamusume import UmaMusumeAPI

async def main():
    # Use UmaMusumeAPI as an async context manager to handle session lifecycle
    async with UmaMusumeAPI() as api:
        # Fetch a list of all basic characters
        characters = await api.fetch_characters()
        print(f"Found {len(characters)} characters!")

        # Fetch detailed information about a specific character
        if characters:
            first_char_id = characters[0].id
            char_detail = await api.fetch_character_detail(first_char_id)
            print(f"Character Name: {char_detail.name}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Disclaimer

This is an **unofficial** wrapper. It is not affiliated with, endorsed by, or sponsored by Gametora or Cygames. Please be respectful of Gametora's servers and utilize the built-in caching features to avoid spamming requests.
