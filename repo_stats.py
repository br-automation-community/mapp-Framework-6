#!/usr/bin/env python3
"""
Repository Statistics Fetcher for mapp-Framework-6

This script fetches and displays repository statistics including:
- Downloads (from releases)
- Forks count
- Clone statistics (views and clones if accessible)
- Stars and other basic metrics

Usage:
    python3 repo_stats.py [--token YOUR_GITHUB_TOKEN]

Note: Some statistics require authentication for private repos or rate limiting.
"""

import requests
import json
import argparse
from datetime import datetime, timedelta
import sys

class RepositoryStats:
    def __init__(self, owner="br-automation-community", repo="mapp-Framework-6", token=None):
        self.owner = owner
        self.repo = repo
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        
        if token:
            self.headers["Authorization"] = f"token {token}"
    
    def _make_request(self, endpoint):
        """Make a request to GitHub API with error handling"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                if not self.token:
                    print(f"⚠️  Rate limited for {endpoint} - consider using --token for higher limits")
                else:
                    print(f"⚠️  Access denied for {endpoint}")
                return None
            elif response.status_code == 404:
                print(f"⚠️  Not found: {endpoint}")
                return None
            else:
                print(f"⚠️  Error {response.status_code} fetching {endpoint}: {response.text[:100]}")
                return None
        except Exception as e:
            print(f"⚠️  Error making request to {endpoint}: {e}")
            return None
    
    def get_repository_info(self):
        """Get basic repository information"""
        return self._make_request(f"repos/{self.owner}/{self.repo}")
    
    def get_releases(self):
        """Get repository releases for download statistics"""
        return self._make_request(f"repos/{self.owner}/{self.repo}/releases")
    
    def get_traffic_clones(self):
        """Get clone statistics (requires push access)"""
        return self._make_request(f"repos/{self.owner}/{self.repo}/traffic/clones")
    
    def get_traffic_views(self):
        """Get view statistics (requires push access)"""
        return self._make_request(f"repos/{self.owner}/{self.repo}/traffic/views")
    
    def calculate_download_stats(self, releases):
        """Calculate download statistics from releases"""
        if not releases:
            return {"total_downloads": 0, "last_year_downloads": 0, "release_count": 0}
        
        total_downloads = 0
        last_year_downloads = 0
        one_year_ago = datetime.now() - timedelta(days=365)
        
        for release in releases:
            release_date = datetime.strptime(release['published_at'], '%Y-%m-%dT%H:%M:%SZ')
            
            for asset in release.get('assets', []):
                downloads = asset.get('download_count', 0)
                total_downloads += downloads
                
                if release_date >= one_year_ago:
                    last_year_downloads += downloads
        
        return {
            "total_downloads": total_downloads,
            "last_year_downloads": last_year_downloads,
            "release_count": len(releases)
        }
    
    def format_number(self, num):
        """Format large numbers with K/M suffixes"""
        if num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        else:
            return str(num)
    
    def display_stats(self):
        """Fetch and display all available statistics"""
        print(f"📊 Repository Statistics for {self.owner}/{self.repo}")
        print("=" * 60)
        
        # Basic repository info
        repo_info = self.get_repository_info()
        if repo_info:
            print(f"⭐ Stars: {self.format_number(repo_info.get('stargazers_count', 0))}")
            print(f"🍴 Forks: {self.format_number(repo_info.get('forks_count', 0))}")
            print(f"👀 Watchers: {self.format_number(repo_info.get('watchers_count', 0))}")
            print(f"🐛 Open Issues: {repo_info.get('open_issues_count', 0)}")
            print(f"📅 Created: {repo_info.get('created_at', 'N/A')[:10]}")
            print(f"🔄 Last Updated: {repo_info.get('updated_at', 'N/A')[:10]}")
            print()
        
        # Download statistics from releases
        print("📦 Download Statistics (Last Year):")
        releases = self.get_releases()
        download_stats = self.calculate_download_stats(releases)
        print(f"   Total Downloads (All Time): {self.format_number(download_stats['total_downloads'])}")
        print(f"   Downloads (Last Year): {self.format_number(download_stats['last_year_downloads'])}")
        print(f"   Number of Releases: {download_stats['release_count']}")
        print()
        
        # Traffic statistics (clones and views)
        print("📈 Traffic Statistics (Last 14 Days):")
        
        clones_data = self.get_traffic_clones()
        if clones_data:
            total_clones = clones_data.get('count', 0)
            unique_clones = clones_data.get('uniques', 0)
            print(f"   Total Clones: {self.format_number(total_clones)}")
            print(f"   Unique Clones: {self.format_number(unique_clones)}")
        else:
            print("   Clone statistics: Not available (requires repository access)")
        
        views_data = self.get_traffic_views()
        if views_data:
            total_views = views_data.get('count', 0)
            unique_views = views_data.get('uniques', 0)
            print(f"   Total Views: {self.format_number(total_views)}")
            print(f"   Unique Views: {self.format_number(unique_views)}")
        else:
            print("   View statistics: Not available (requires repository access)")
        
        print()
        print("💡 Note: Traffic statistics (clones/views) require repository access")
        print("   and only show data for the last 14 days per GitHub API limitations.")
        print("   For historical data beyond 14 days, consider using GitHub Insights")
        print("   directly on the repository page.")

def main():
    parser = argparse.ArgumentParser(description="Fetch repository statistics")
    parser.add_argument("--token", help="GitHub personal access token for authenticated requests")
    parser.add_argument("--owner", default="br-automation-community", help="Repository owner")
    parser.add_argument("--repo", default="mapp-Framework-6", help="Repository name")
    
    args = parser.parse_args()
    
    stats = RepositoryStats(args.owner, args.repo, args.token)
    stats.display_stats()

if __name__ == "__main__":
    main()