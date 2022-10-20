from abc import ABC, abstractmethod

class ABCKafDataLoader(ABC):

    '''
    Абстрактный класс-загрузчик данных на каждую кафедру
    В наследниках должен быть имплементирован метод get_kaf_info, который по названию кафедры возвращает словарь
    со всей доступной информацией по приему на направления которые реализуются на кафедре
    '''

    @abstractmethod
    def get_kaf_info(self, kaf_name: str) -> dict:
        pass