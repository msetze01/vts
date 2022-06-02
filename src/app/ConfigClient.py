from abc import abstractmethod


class ConfigClient:
    @abstractmethod
    def get_extend_pw(self):
        pass
