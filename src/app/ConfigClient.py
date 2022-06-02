from abc import abstractmethod


class ConfigClient:
    @abstractmethod
    def _get_extend_pw(self):
        pass
