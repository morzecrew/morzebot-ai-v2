from db.repository.settings_repository import get_settings_by_uid


class Settings:
    def __init__(self, uuid):
        self.uuid = uuid

    def is_speller_enabled(self):
        settings = get_settings_by_uid(self.uuid)
        return settings["spell_check_enabled"]
