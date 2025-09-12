# Repository Statistics Documentation

This document explains how to view statistics for the mapp-Framework-6 repository, including downloads, forks, clones, and other metrics for the last year.

## Available Statistics

### Basic Metrics
- ⭐ Stars count
- 🍴 Forks count  
- 👀 Watchers count
- 🐛 Open issues count
- 📅 Repository creation date
- 🔄 Last update date

### Download Statistics
- 📦 Total downloads from all releases
- 📦 Downloads in the last year
- 📦 Number of releases

### Traffic Statistics (Last 14 Days)
- 📊 Total repository clones
- 📊 Unique clones
- 📊 Total repository views
- 📊 Unique views

## How to Use

### Option 1: Basic Statistics (No Authentication Required)
```bash
python3 basic_stats.py
```

This displays basic repository information and links to GitHub's built-in analytics.

### Option 2: Detailed Statistics (Requires GitHub Token)
```bash
python3 repo_stats.py --token YOUR_GITHUB_TOKEN
```

This fetches real-time statistics from the GitHub API.

#### Getting a GitHub Token
1. Go to GitHub.com → Settings → Developer settings → Personal access tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (for private repos) or `public_repo` (for public repos)
4. Copy the generated token

### Option 3: GitHub Web Interface
Visit the repository's [Insights page](https://github.com/br-automation-community/mapp-Framework-6/pulse) for:
- Traffic analytics
- Contributor statistics
- Code frequency
- Network graphs
- Dependency insights

## Limitations

- **Traffic Data**: GitHub API only provides traffic statistics for the last 14 days
- **Historical Data**: For data beyond 14 days, use GitHub's web interface
- **Rate Limiting**: Unauthenticated requests are limited to 60 per hour
- **Access Requirements**: Some statistics require repository access permissions

## Examples

### Basic Usage
```bash
# Show basic repository information
python3 basic_stats.py

# Show detailed statistics with authentication
python3 repo_stats.py --token ghp_xxxxxxxxxxxx

# Specify different repository
python3 repo_stats.py --owner myorg --repo myrepo
```

### Sample Output
```
📊 Repository Statistics for br-automation-community/mapp-Framework-6
============================================================
⭐ Stars: 0
🍴 Forks: 0
👀 Watchers: 0
🐛 Open Issues: 6
📅 Created: 2025-07-01
🔄 Last Updated: 2025-07-03

📦 Download Statistics (Last Year):
   Total Downloads (All Time): 0
   Downloads (Last Year): 0
   Number of Releases: 0

📈 Traffic Statistics (Last 14 Days):
   Total Clones: 50
   Unique Clones: 25
   Total Views: 150
   Unique Views: 75
```

## Troubleshooting

### Common Issues
1. **Rate Limited**: Use authentication token for higher limits
2. **Access Denied**: Ensure token has correct permissions
3. **No Traffic Data**: Traffic statistics require repository access

### Getting Help
- Check the GitHub API documentation: https://docs.github.com/en/rest
- Repository issues: https://github.com/br-automation-community/mapp-Framework-6/issues
- GitHub support: https://support.github.com