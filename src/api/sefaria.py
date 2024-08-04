from dataclasses import dataclass
import json
import requests
import typing

SEFARIA_API_BASE = "https://www.sefaria.org/api"

# Models
# TODO: Rework this structure - we'll need an index model and a text model.
# don't worry about storing text right now, download that when a text is selected.
# Then we can store the text in sqlite and pull from it as needed.

class SefariaResponse:
    pass
class SefariaResponse:
    def __init__(self):
        pass
    
    def as_payload(dct) -> SefariaResponse:
        return SefariaResponse()

    def from_response(json_response: str) -> SefariaResponse:
        return SefariaResponse()


class SefariaText(SefariaResponse):
    title: str = None
    commentator: str = None
    base_text_order: int = None # optional
    corpus: str = None # optional
    collectiveTitle: str = None
    dependence: str = None
    primary_category: str = None
    categories: list[str] = None
    base_text_titles: list[str] = None
    
    def __init__(self, categories):
        pass


class SefariaContent(SefariaResponse):
    pass

class SefariaIndex(SefariaResponse):
    pass
class SefariaIndex(SefariaResponse):
    category: str = None
    enShortDesc: str = None
    contents: list = None

    def from_dict(dct, depth) -> SefariaIndex:
        return SefariaIndex(dct.get('category', None), dct['enShortDesc'], dct.get('contents', None), depth)

    def __init__(self, category, enShortDesc, contents, depth):
        self.category = category
        self.enShortDesc = enShortDesc
        
        if contents is not None:
            self.contents = []
            for dct in contents:
                if 'title' in dct:
                    print('    ' + dct['title'])
                elif 'category' in dct:
                    print("" + str(depth) + " " + dct['category'])
                    self.contents.append(SefariaIndex.from_dict(dct, depth + 1))

# API communicator

class SefariaAPI:
    def __init__(self):
        pass

    @classmethod
    def _get(self, stub: str):
        url = f'{SEFARIA_API_BASE}/{stub}'
        response = requests.get(url)
        body = json.loads(response.content)
        return body

    @classmethod
    def get_indices(self) -> list[SefariaIndex]:
        result: list[SefariaIndex] = []
        body = self._get('index')
        for dct in body:
            result.append(SefariaIndex.from_dict(dct, 0))
        return result
