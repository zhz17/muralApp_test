import requests
import json
import logging
import copy

logger = logging.getLogger(__name__)

class MuralClient:
    def __init__(self, auth_token, workspace_id):
        self.auth_token = auth_token
        self.workspace_id = workspace_id
        self.base_url = "https://app.mural.co/api/public/v1"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }

    @staticmethod
    def exchange_auth_code(client_id, client_secret, redirect_uri, code):
        url = "https://app.mural.co/api/public/v1/authorization/oauth2/token"
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error exchanging auth code: {e}")
            if response and response.text:
                logger.error(f"Response: {response.text}")
            raise

    def create_room(self, room_name):
        url = f"{self.base_url}/rooms"
        payload = {
            "workspaceId": self.workspace_id,
            "name": room_name,
            "type": "open"
        }
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["value"]["id"]
        except Exception as e:
            logger.error(f"Error creating room {room_name}: {e}")
            if response and response.text:
                logger.error(f"Response: {response.text}")
            raise

    def create_folder(self, room_id, folder_name):
        url = f"{self.base_url}/rooms/{room_id}/folders"
        payload = {"name": folder_name}
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["value"]["id"]
        except Exception as e:
            logger.error(f"Error creating folder {folder_name}: {e}")
            raise

    def create_mural(self, room_id, folder_id, title):
        url = f"{self.base_url}/murals"
        payload = {
            "workspaceId": self.workspace_id,
            "roomId": int(room_id),
            "folderId": folder_id,
            "title": title
        }
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["value"]["id"]
        except Exception as e:
            logger.error(f"Error creating mural {title}: {e}")
            if response and response.text:
                 logger.error(f"Response: {response.text}")
            raise

    def add_widget(self, mural_id, widget_data):
        widget_type_map = {
            "sticky note": "sticky-note",
            "shape": "shape",
            "text": "textbox"
        }
        
        original_type = widget_data.get("type")
        if original_type not in widget_type_map:
            logger.warning(f"Unknown widget type: {original_type}")
            return

        api_widget_type = widget_type_map[original_type]
        url = f"{self.base_url}/murals/{mural_id}/widgets/{api_widget_type}"
        
        payload = copy.deepcopy(widget_data)
        if "type" in payload:
            del payload["type"]

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            logger.info(f"Added widget to mural {mural_id}")
        except Exception as e:
            logger.error(f"Error adding widget to mural {mural_id}: {e}")
            if response and response.text:
                logger.error(f"Response: {response.text}")
            # Don't raise here, just log error so other widgets can still be added
            pass

    def process_json(self, murals_data):
        rooms_created = {}
        folders_created = {}

        results = []

        for mural_def in murals_data:
            # 1. Handle Room
            room_name = mural_def.get("room", {}).get("name")
            room_id = mural_def.get("room", {}).get("id")
            
            if not room_id:
                if room_name in rooms_created:
                    room_id = rooms_created[room_name]
                else:
                    try:
                        room_id = self.create_room(room_name)
                        rooms_created[room_name] = room_id
                    except Exception as e:
                        results.append(f"Failed to create room '{room_name}': {str(e)}")
                        continue

            # 2. Handle Folder
            folder_name = mural_def.get("folder", {}).get("name")
            folder_id = mural_def.get("folder", {}).get("id")

            if folder_name and not folder_id:
                if folder_name in folders_created:
                    folder_id = folders_created[folder_name]
                else:
                    try:
                        folder_id = self.create_folder(room_id, folder_name)
                        folders_created[folder_name] = folder_id
                    except Exception as e:
                        results.append(f"Failed to create folder '{folder_name}' in room '{room_name}': {str(e)}")
                        continue
            
            # 3. Create Mural
            mural_title = mural_def.get("mural_name")
            try:
                mural_id = self.create_mural(room_id, folder_id, mural_title)
                results.append(f"Created Mural: {mural_title} (ID: {mural_id})")
            except Exception as e:
                results.append(f"Failed to create mural '{mural_title}': {str(e)}")
                continue

            # 4. Add Widgets
            widgets = mural_def.get("widgets_arr", [])
            for widget in widgets:
                self.add_widget(mural_id, widget)
        
        return results
