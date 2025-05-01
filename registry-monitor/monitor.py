#!/usr/bin/env python3
import os
import time
import json
import logging
import subprocess
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("RegistryMonitor")

# Registry details
REGISTRY_URL = "http://registry.dev.svc.cluster.local:5000"
APP_NAME = "my-webapp"
DEPLOYMENT_NAME = "my-webapp"
CONTAINER_NAME = "web-container"
CHECK_INTERVAL = 30  # seconds

# Keep track of the latest tag we've seen
latest_processed_tag = None

def get_tags():
    """Get all tags for the application from the registry"""
    try:
        response = requests.get(f"{REGISTRY_URL}/v2/{APP_NAME}/tags/list")
        if response.status_code == 200:
            return response.json().get("tags", [])
        else:
            logger.error(f"Failed to get tags: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        logger.error(f"Error getting tags: {str(e)}")
        return []

def get_newest_tag(tags):
    """Find the newest tag based on v1, v2, etc. naming convention"""
    version_tags = [tag for tag in tags if tag.startswith('v')]
    if not version_tags:
        return None
    
    # Sort version tags
    version_tags.sort(key=lambda x: int(x[1:]) if x[1:].isdigit() else 0, reverse=True)
    return version_tags[0]

def update_deployment(tag):
    """Update the Kubernetes deployment with the new image tag"""
    try:
        new_image = f"registry.dev.svc.cluster.local:5000/{APP_NAME}:{tag}"
        logger.info(f"Updating deployment {DEPLOYMENT_NAME} with image {new_image}")
        
        cmd = f"kubectl set image deployment/{DEPLOYMENT_NAME} {CONTAINER_NAME}={new_image}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info(f"Successfully updated deployment to {tag}")
            return True
        else:
            logger.error(f"Failed to update deployment: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error updating deployment: {str(e)}")
        return False

def main():
    global latest_processed_tag
    
    logger.info("Registry monitor started")
    
    while True:
        try:
            tags = get_tags()
            if tags:
                newest_tag = get_newest_tag(tags)
                logger.info(f"Found tags: {tags}, newest: {newest_tag}")
                
                if newest_tag and newest_tag != latest_processed_tag:
                    logger.info(f"New version detected: {newest_tag}")
                    if update_deployment(newest_tag):
                        latest_processed_tag = newest_tag
                    
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            logger.error(f"Error in monitor loop: {str(e)}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
