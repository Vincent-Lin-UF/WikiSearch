import json
import logging

class Database:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.graph = self.load_json_graph()
        logging.info(f"Loaded fake Wikipedia graph with {len(self.graph)} nodes")

    def load_json_graph(self):
        with open(self.json_file_path, 'r') as f:
            return json.load(f)

    def fetch_page(self, page_title):
        if isinstance(page_title, int):
            page_id = str(page_title)
            if page_id in self.graph:
                return (int(page_id), self.graph[page_id]['title'], False)
        else:
            for page_id, page_data in self.graph.items():
                if page_data['title'].lower() == page_title.lower():
                    return (int(page_id), page_data['title'], False)
        raise ValueError(f'Invalid page title or ID {page_title} provided. Page does not exist.')

    def fetch_outgoing_links(self, page_id):
        page_id = str(page_id) 
        if page_id in self.graph:
            return self.graph[page_id]['outgoing_links']
        return []

    def autocomplete(self, query):
        query = query.lower()
        return [page['title'] for page in self.graph.values() if page['title'].lower().startswith(query)][:10]

    def get_status(self):
        return {"pages": len(self.graph)}