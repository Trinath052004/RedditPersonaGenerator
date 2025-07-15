# Note
Trinath1405 and Trinath052004 both accounts belong to me.
# Reddit User Persona Generator

A Python script that scrapes Reddit user data, analyzes posting patterns, and generates comprehensive user personas with detailed citations.

## Features

- Scrapes Reddit user posts and comments using PRAW (Python Reddit API Wrapper)
- Analyzes user behavior patterns, interests, and activity
- Generates detailed user personas with evidence-based characteristics
- Provides citations with direct links to supporting posts/comments
- Outputs comprehensive text-based persona reports

## Requirements

- Python 3.7+
- Reddit API credentials (client ID, client secret)
- Required Python packages (see Installation section)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/reddit-persona-generator.git
cd reddit-persona-generator
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up Reddit API credentials:
   - Go to https://www.reddit.com/prefs/apps
   - Create a new application (script type)
   - Create a `.env` file in the project root with your credentials:

```
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=PersonaGenerator/1.0
```

## Usage

1. Run the script:
```bash
python reddit_persona_generator.py
```

2. Enter a Reddit profile URL when prompted:
   - Example: `https://www.reddit.com/user/spez`
   - Example: `https://www.reddit.com/user/username`

3. The script will:
   - Scrape the user's recent posts and comments
   - Analyze their activity patterns and interests
   - Generate a comprehensive persona report
   - Save the results to `username_persona.txt`

## Output Format

The generated persona includes:

- **Basic Information**: Account age, karma, activity statistics
- **Interests**: Primary subreddits and topics of engagement
- **Personality Traits**: Behavioral patterns derived from content analysis
- **Activity Patterns**: Peak activity times and posting frequency
- **Expertise Areas**: Topics where the user demonstrates knowledge
- **Citations**: Direct links to posts/comments supporting each characteristic

## Example Output Files

The repository includes sample persona files for the provided test users:
- `kojied_persona.txt`
- `Hungry-Move-6603_persona.txt`

## Technical Details

### Data Analysis
- Analyzes posting frequency and timing patterns
- Identifies primary subreddits and topics of interest
- Performs content analysis for personality trait detection
- Tracks karma patterns and engagement levels

### Privacy & Ethics
- Only analyzes publicly available Reddit data
- Provides citations to original sources
- Respects Reddit's API terms of service
- Does not store or redistribute user data

## Code Structure

```
reddit_persona_generator.py    # Main script
requirements.txt               # Python dependencies
.env                          # API credentials (not included)
README.md                     # This file
sample_outputs/               # Example persona files
├── kojied_persona.txt
└── Hungry-Move-6603_persona.txt
```

## Dependencies

- `praw` - Python Reddit API Wrapper
- `python-dotenv` - Environment variable management
- `textblob` - Text processing and sentiment analysis
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing (if needed)

## API Rate Limits

The script respects Reddit's API rate limits:
- Maximum 100 requests per minute
- Built-in delays between requests
- Graceful error handling for rate limit issues

## Testing

Test the script with the provided example URLs:
- https://www.reddit.com/user/kojied/
- https://www.reddit.com/user/Hungry-Move-6603/


### Common Issues

1. **"Invalid Reddit profile URL" error**
   - Ensure the URL follows the format: `https://www.reddit.com/user/username`
   - Check that the username exists and is public

2. **API authentication errors**
   - Verify your `.env` file contains correct credentials
   - Ensure your Reddit app is configured as a "script" type

3. **Rate limiting**
   - The script includes built-in delays
   - If you hit rate limits, wait a few minutes before retrying

4. **Empty or minimal output**
   - User may have very few public posts/comments
   - Some users have private profiles or deleted content

*Created as part of a data analysis assignment focusing on social media user behavior analysis.*
