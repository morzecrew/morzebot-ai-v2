from db.repository.settings_repository import get_settings_by_uuid


class Settings:
    def __init__(self, uuid):
        self.uuid = uuid

    def is_speller_enabled(self):
        settings = get_settings_by_uuid(self.uuid)
        return settings["data"]["spell_check_enabled"]
