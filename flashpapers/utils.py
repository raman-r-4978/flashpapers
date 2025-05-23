import json
import logging
import re
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Union

import requests

logger = logging.getLogger(__name__)


def save_json(config: Dict[str, Any], file_path: str, mode: str = "a") -> None:
    """Saves the given configuration dictionary to a JSON file."""
    try:
        with open(file_path, mode=mode) as f:
            json.dump(config, f, indent=4, default=str)  # Use default=str for datetime etc.
    except IOError as e:
        logger.error(f"IOError while saving config to {file_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error saving config to {file_path}: {e}")
        raise


def load_json(file_path: str) -> Union[Dict[str, Any], List[Any]]:
    """Loads a JSON file and returns its content as a dictionary."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"File {file_path} not found.")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error for file {file_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading JSON from {file_path}: {e}")
        raise


def fetch_from_arxiv(arxiv_id: str) -> Optional[Dict[str, Any]]:
    # """Fetches paper metadata from the arXiv API."""
    # arxiv_id = arxiv_id.strip()
    # # Basic validation of arXiv ID format (e.g., 2106.04554 or cs/0112017v1)
    # if not re.match(r"^\d{4}\.\d{4,5}(v\d+)?$|^[a-z\-]+(\.[A-Z]{2})?\/\d{7}(v\d+)?$", arxiv_id):
    #     logger.warning(f"Invalid arXiv ID format: {arxiv_id}")
    #     # Optionally raise an error or return None with a message
    #     # For now, let the API call fail naturally if it's truly invalid.
    #     pass

    # api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    # logger.info(f"Fetching from arXiv: {api_url}")

    # try:
    #     response = requests.get(api_url)
    #     response.raise_for_status()  # Raise an error for bad responses
    #     data = response.text
    #     # Parse the XML response
    #     root = ET.fromstring(data)
    #     ns = {"arxiv": "http://arxiv.org/schemas/atom"}
    #     entry = root.find("arxiv:entry", ns)
    #     if entry is None:
    #         logger.warning(f"No entry found for arXiv ID: {arxiv_id}")
    #         return None
    #     title = entry.find("arxiv:title", ns).text
    #     authors = [
    #         author.find("arxiv:name", ns).text for author in entry.findall("arxiv:author", ns)
    #     ]
    #     abstract = entry.find("arxiv:summary", ns).text
    #     categories = [cat.text for cat in entry.findall("arxiv:category", ns)]
    #     link = entry.find("arxiv:id", ns).text
    #     # Convert to a dictionary
    #     paper_info = {
    #         "paper_title": title,
    #         "authors": ", ".join(authors),
    #         "background_of_the_study": abstract,
    #         "research_objectives_and_hypothesis": "",
    #         "methodology": "",
    #         "results_and_findings": "",
    #         "discussion_and_interpretation": "",
    #         "contributions_to_the_field": "",
    #         "achievements_and_significance": "",
    #         "link": link,
    #         "notes": "",
    #         "keywords": ", ".join(categories),
    #         "category": categories,
    #     }
    #     return paper_info
    # except requests.RequestException as e:
    #     logger.error(f"Request error while fetching from arXiv: {e}")
    #     raise

    # Version 2.0 of the function
    #             try:
    #                 # Extract ID from URL if necessary
    #                 if "arxiv.org/abs/" in arxiv_id:
    #                     arxiv_id = arxiv_id.split("arxiv.org/abs/")[-1]

    #                 # Clean any potential URL parameters
    #                 arxiv_id = arxiv_id.split("?")[0].split("#")[0].strip()

    #                 # Fetch paper data from arXiv
    #                 paper_data = fetch_from_arxiv(arxiv_id)

    #                 if not paper_data:
    #                     st.error(f"Could not find paper with ID: {arxiv_id}")
    #                     return None

    #                 # Format the data to match our structure
    #                 flashpaper = {
    #                     "paper_title": paper_data.get("title", ""),
    #                     "authors": ", ".join(paper_data.get("authors", [])),
    #                     "background_of_the_study": "",
    #                     "research_objectives_and_hypothesis": "",
    #                     "methodology": "",
    #                     "results_and_findings": "",
    #                     "discussion_and_interpretation": "",
    #                     "contributions_to_the_field": "",
    #                     "achievements_and_significance": "",
    #                     "link": paper_data.get("url", ""),
    #                     "notes": "",
    #                     "keywords": paper_data.get("categories", []),
    #                     "category": category,
    #                     "added_date": datetime.today(),
    #                     "next_review_date": datetime.today(),
    #                 }

    #                 # Add abstract to notes if available
    #                 if paper_data.get("abstract"):
    #                     flashpaper["notes"] = f"Abstract: {paper_data['abstract']}"

    #                 # Show a preview of the imported data
    #                 st.success("Paper found! Review the details below:")
    #                 st.write(f"**Title:** {flashpaper['paper_title']}")
    #                 st.write(f"**Authors:** {flashpaper['authors']}")
    #                 st.write(f"**Link:** {flashpaper['link']}")
    #                 if paper_data.get("abstract"):
    #                     st.write("**Abstract:**")
    #                     st.write(paper_data["abstract"])

    #                 # Confirm import
    #                 if st.button("Confirm Import"):
    #                     return flashpaper

    #             except Exception as e:
    #                 logger.error(f"Error fetching from arXiv: {e}")
    #                 st.error(f"Failed to fetch paper: {str(e)}")
    #                 return None

    # return None
    pass
