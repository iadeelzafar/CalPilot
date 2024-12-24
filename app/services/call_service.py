"""
CallService: Core service for managing and processing call data.
Developed by Adeel Zafar (www.adeelzafar.com)
"""

from datetime import datetime, timezone
import json
import re
from collections import defaultdict
from typing import List, Dict, Optional
import os
from functools import lru_cache
from google.cloud import storage

class CallService:
    def __init__(self, app):
        self.logger = app.logger
        self.calls_file = app.config['CALLS_FILE']
        self.bucket_name = app.config.get('GCS_BUCKET')
        self._calls_cache = None
        self._calls_cache_timestamp = None

        # Check local file in development
        if not self.bucket_name and not os.path.exists(self.calls_file):
            self.logger.error(f"Calls file not found: {self.calls_file}")
            raise FileNotFoundError(f"Calls file not found: {self.calls_file}")

    def _load_from_gcs(self) -> str:
        """Load calls data from Google Cloud Storage if configured, else from local file."""
        if not self.bucket_name:
            self.logger.debug("Using local file storage")
            with open(self.calls_file, 'r') as f:
                return f.read()
        
        try:
            self.logger.debug(f"Loading from GCS bucket: {self.bucket_name}")
            storage_client = storage.Client()
            bucket = storage_client.bucket(self.bucket_name)
            blob = bucket.blob('calls.json')
            return blob.download_as_text()
        except Exception as e:
            self.logger.error(f"Error loading from GCS: {str(e)}")
            raise

    def _should_reload_cache(self) -> bool:
        """Check if we need to reload the cache based on environment."""
        if self._calls_cache is None or self._calls_cache_timestamp is None:
            return True
            
        try:
            if self.bucket_name:
                # In production, refresh cache every 5 minutes
                cache_age = datetime.now().timestamp() - self._calls_cache_timestamp
                return cache_age > 300
            else:
                # In development, check file modification time
                current_mtime = os.path.getmtime(self.calls_file)
                return current_mtime > self._calls_cache_timestamp
        except OSError:
            return True

    def load_calls(self) -> List[Dict]:
        """Load and process calls from file with caching."""
        if not self._should_reload_cache():
            self.logger.debug("Using cached calls data")
            return self._calls_cache

        try:
            self.logger.info(f"Loading calls from {self.calls_file}")
            data = self._load_from_gcs()
            calls = json.loads(data)
            
            processed_calls = []
            for call in calls:
                try:
                    processed_call = self._process_call(call)
                    processed_calls.append(processed_call)
                except Exception as e:
                    self.logger.error(f"Error processing call {call.get('id', 'unknown')}: {str(e)}")
                    continue
            
            # Update cache
            self._calls_cache = processed_calls
            self._calls_cache_timestamp = datetime.now().timestamp()
            
            self.logger.info(f"Successfully loaded {len(processed_calls)} calls")
            return processed_calls
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in calls file: {str(e)}")
            return []
        except Exception as e:
            self.logger.error(f"Error loading calls: {str(e)}")
            return []

    def refresh_cache(self) -> None:
        """Force refresh the calls cache."""
        self._calls_cache = None
        self._calls_cache_timestamp = None
        self.load_calls()

    @staticmethod
    @lru_cache(maxsize=128)
    def format_duration(seconds: float) -> str:
        """Format duration in a human-readable way (hours, minutes, seconds)."""
        hours = int(seconds // 3600)
        remaining = seconds % 3600
        minutes = int(remaining // 60)
        remaining_seconds = int(remaining % 60)
        
        if hours > 0:
            if minutes == 0:
                return f"{hours}h"  # Return just hours if no minutes
            if remaining_seconds == 0:
                return f"{hours}h {minutes}m"
            return f"{hours}h {minutes}m {remaining_seconds}s"
        elif minutes > 0:
            if remaining_seconds == 0:
                return f"{minutes}m"
            return f"{minutes}m {remaining_seconds}s"
        return f"{remaining_seconds}s"

    def _process_call(self, call: Dict) -> Dict:
        """Process a single call record."""
        try:
            # Validate required fields
            required_fields = ['id', 'created_at_utc', 'call_metadata', 'transcript']
            missing_fields = [field for field in required_fields if field not in call]
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            call['formatted_date'] = datetime.fromisoformat(
                call['created_at_utc'].replace('Z', '+00:00')
            ).strftime('%B %d, %Y')
            
            # Format duration in a readable way
            duration_seconds = call['call_metadata']['duration']
            call['duration_mins'] = self.format_duration(duration_seconds)
            
            # Extract companies from email domains
            call['companies'] = list(set([
                party['email'].split('@')[1].split('.')[0] 
                for party in call['call_metadata']['parties'] 
                if party.get('email')
            ]))
            
            # Extract keywords from transcript
            call['keywords'] = self._extract_keywords(call['transcript']['text'])
            
            return call
        except Exception as e:
            raise ValueError(f"Error processing call: {str(e)}")

    def get_call_by_id(self, call_id: str) -> Optional[Dict]:
        """Get a specific call by ID."""
        if not call_id:
            self.logger.error("Call ID cannot be empty")
            return None
            
        self.logger.debug(f"Fetching call with ID: {call_id}")
        calls = self.load_calls()
        call = next((c for c in calls if c['id'] == call_id), None)
        
        if call is None:
            self.logger.info(f"Call not found with ID: {call_id}")
        return call

    def search_calls(self, query: str = '', company: str = '', date_from: str = '', date_to: str = '') -> List[Dict]:
        """Search calls with optional filters."""
        self.logger.info(f"Searching calls with query='{query}', company='{company}', date_from='{date_from}', date_to='{date_to}'")
        calls = self.load_calls()
        
        try:
            if query:
                query = query.lower()
                calls = [
                    call for call in calls 
                    if query in call['call_metadata']['title'].lower() or
                       query in call['transcript']['text'].lower()
                ]
            
            if company:
                calls = [
                    call for call in calls 
                    if company in call['companies']
                ]
            
            if date_from or date_to:
                try:
                    if date_from:
                        date_from = datetime.fromisoformat(date_from).replace(tzinfo=timezone.utc)
                    if date_to:
                        date_to = datetime.fromisoformat(date_to).replace(tzinfo=timezone.utc)

                    calls = [
                        call for call in calls
                        if (not date_from or datetime.fromisoformat(call['created_at_utc'].replace('Z', '+00:00')) >= date_from)
                        and (not date_to or datetime.fromisoformat(call['created_at_utc'].replace('Z', '+00:00')) <= date_to)
                    ]
                except ValueError as e:
                    self.logger.error(f"Invalid date format: {str(e)}")
            
            self.logger.info(f"Found {len(calls)} matching calls")
            return calls
            
        except Exception as e:
            self.logger.error(f"Error during call search: {str(e)}")
            return []

    def get_call_summary(self, call_id: str) -> Optional[Dict]:
        """Get summary information for a specific call."""
        if not call_id:
            self.logger.error("Call ID cannot be empty")
            return None
            
        self.logger.debug(f"Generating summary for call ID: {call_id}")
        call = self.get_call_by_id(call_id)
        if not call:
            self.logger.info(f"Cannot generate summary: Call not found with ID: {call_id}")
            return None

        try:
            summary = {
                'duration_mins': call['duration_mins'],
                'participant_count': len(call['call_metadata']['parties']),
                'companies': call['companies'],
                'keywords': call['keywords'],
                'summary': call['inference_results'].get('call_summary', '')
            }
            return summary
        except Exception as e:
            self.logger.error(f"Error generating summary for call {call_id}: {str(e)}")
            return None

    @lru_cache(maxsize=1)
    def get_unique_companies(self) -> List[str]:
        """Get a sorted list of all unique companies with caching."""
        self.logger.debug("Fetching unique companies list")
        try:
            calls = self.load_calls()
            companies = sorted(list(set(
                company 
                for call in calls 
                for company in call['companies']
            )))
            self.logger.info(f"Found {len(companies)} unique companies")
            return companies
        except Exception as e:
            self.logger.error(f"Error fetching unique companies: {str(e)}")
            return []

    def _extract_keywords(self, text: str) -> Dict[str, List[str]]:
        """Extract important keywords and their context from text."""
        if not text:
            return {}
            
        try:
            important_terms = [
                'pricing', 'budget', 'timeline', 'implementation', 'integration',
                'decision', 'approval', 'concerns', 'requirements', 'next steps',
                'follow up', 'demo', 'trial', 'features', 'competition'
            ]
            
            keywords = defaultdict(list)
            for term in important_terms:
                matches = re.finditer(f"[^.]*{term}[^.]*\\.", text.lower())
                for match in matches:
                    keywords[term].append(match.group().strip())
                    
            return dict(keywords)
        except Exception as e:
            self.logger.error(f"Error extracting keywords: {str(e)}")
            return {} 