import os
import requests


def scrape_linkedin_profile(linkedin_profile_url: str, fake: bool = False) -> dict:
    """Scrape information from a LinkedIn profile,
    Manually scrape the information from a LinkedIn profile."""

    if fake:
        api_endpoint = (
            "https://gist.githubusercontent.com/timbogit/9dee5134cc6c543731525e1f54683cef/raw"
            "/2cea675cafb3f0723b77b73f78ec529172a70532/linkedin_tim.json"
        )
        header_dic = {}
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}

    response = requests.get(
        api_endpoint, params={"url": linkedin_profile_url}, headers=header_dic
    )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications", "experiences"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data
