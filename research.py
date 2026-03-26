#!/usr/bin/env python3
"""
Moonshot Opportunities - AI Moonshot Research Tool
Discovers and analyzes high-potential AI opportunities
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os


class MoonshotResearcher:
    """Research AI moonshot opportunities from various sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Moonshot-Researcher/1.0"
        })
    
    def get_github_trending_ai(self, days: int = 30, lang: str = "python") -> List[Dict]:
        """Fetch trending AI repositories from GitHub"""
        try:
            from datetime import datetime, timedelta
            # Get date for query
            date_since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            
            # Get trending repos via GitHub search
            query = f"ai OR ml OR machine-learning OR llm OR artificial-intelligence stars:>100"
            url = f"https://api.github.com/search/repositories"
            params = {"q": query, "sort": "stars", "order": "desc", "per_page": 10}
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return [{
                "name": repo["full_name"],
                "stars": repo["stargazers_count"],
                "description": repo["description"],
                "url": repo["html_url"],
                "language": repo.get("language"),
                "forks": repo.get("forks_count", 0)
            } for repo in data.get("items", [])]
        except Exception as e:
            print(f"Error fetching GitHub trending: {e}")
            return []
    
    def get_hackernews_ai(self, limit: int = 10) -> List[Dict]:
        """Fetch top AI stories from Hacker News"""
        try:
            # Get top stories
            response = self.session.get(
                "https://hacker-news.firebaseio.com/v0/topstories.json",
                timeout=10
            )
            response.raise_for_status()
            story_ids = response.json()[:limit * 2]  # Get more to filter
            
            results = []
            for story_id in story_ids:
                story_resp = self.session.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                    timeout=10
                )
                story = story_resp.json()
                
                # Filter for AI-related stories
                if story and story.get("title"):
                    title_lower = story["title"].lower()
                    if any(kw in title_lower for kw in ["ai", "llm", "gpt", "machine learning", "openai", "anthropic", "ml"]):
                        results.append({
                            "title": story["title"],
                            "url": story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                            "score": story.get("score", 0),
                            "comments": story.get("descendants", 0)
                        })
                if len(results) >= limit:
                    break
            
            return results
        except Exception as e:
            print(f"Error fetching Hacker News: {e}")
            return []
    
    def analyze_opportunity(self, opportunity: Dict) -> Dict:
        """Analyze an opportunity and return structured data"""
        score = 0
        
        # Star power
        if opportunity.get("stars", 0) > 1000:
            score += 3
        elif opportunity.get("stars", 0) > 500:
            score += 2
        elif opportunity.get("stars", 0) > 100:
            score += 1
        
        # Score for HN
        if opportunity.get("score", 0) > 100:
            score += 3
        elif opportunity.get("score", 0) > 50:
            score += 2
        
        return {
            **opportunity,
            "moonshot_score": score,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_report(self) -> Dict:
        """Generate a comprehensive moonshot opportunities report"""
        report = {
            "generated_at": datetime.now().isoformat(),
            "sources": {
                "github_trending": self.get_github_trending_ai(),
                "hackernews": self.get_hackernews_ai()
            }
        }
        
        # Score all opportunities
        all_opportunities = []
        for opp in report["sources"]["github_trending"]:
            all_opportunities.append(self.analyze_opportunity(opp))
        for opp in report["sources"]["hackernews"]:
            all_opportunities.append(self.analyze_opportunity(opp))
        
        # Sort by moonshot score
        all_opportunities.sort(key=lambda x: x.get("moonshot_score", 0), reverse=True)
        report["top_opportunities"] = all_opportunities[:15]
        
        return report
    
    def print_report(self):
        """Print a human-readable report"""
        report = self.generate_report()
        
        print("\n" + "="*60)
        print("🚀 MOONSHOT OPPORTUNITIES REPORT")
        print("="*60)
        print(f"Generated: {report['generated_at']}")
        
        print("\n📊 TOP OPPORTUNITIES:")
        print("-"*60)
        
        for i, opp in enumerate(report["top_opportunities"], 1):
            score = opp.get("moonshot_score", 0)
            stars = opp.get("stars", opp.get("score", 0))
            print(f"\n{i}. {opp.get('name', opp.get('title', 'N/A'))}")
            print(f"   Score: {'⭐' * score} ({score}/6)")
            print(f"   Stars/Points: {stars}")
            print(f"   URL: {opp.get('url', 'N/A')}")
            desc = opp.get('description', '')
            if desc:
                print(f"   Description: {desc[:100]}...")
        
        print("\n" + "="*60)
        return report


def main():
    """Main entry point"""
    researcher = MoonshotResearcher()
    
    # Generate and print report
    report = researcher.print_report()
    
    # Save report to JSON
    output_file = "moonshot_report.json"
    with open(output_file, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📁 Report saved to: {output_file}")
    return report


if __name__ == "__main__":
    main()