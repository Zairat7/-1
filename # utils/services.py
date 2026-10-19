# utils/services.py
import json
from models import Review

class ReviewProcessor:
    """Класс 2: Инкапсулирует чтение JSON и кастомную сортировку"""

    @staticmethod
    def load_from_json(file_path: str) -> list:
        """Чтение JSON-файла с использованием менеджера контекста with"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            # Обработка ошибок для защиты (вопрос по битому JSON)
            print(f"Ошибка при чтении файла: {e}")
            return []

    @classmethod
    def _calculate_weight(cls, review) -> float:
        """
        Составной критерий: приоритет высокому/низкому рейтингу + длине текста.
        Чем больше возвращаемое число, тем выше отзыв в списке.
        """
        # Превращаем объект (модель или словарь) в единый формат для сортировки
        rating = review.rating if isinstance(review, Review) else review.get('rating', 0)
        text = review.text if isinstance(review, Review) else review.get('text', '')
        
        # Формула: длина текста имеет значение, но рейтинг весит больше
        return float(rating) * 10 + (len(text) * 0.05)

    @classmethod
    def merge_sort(cls, arr: list) -> list:
        """
        Кастомный алгоритм: Сортировка слиянием (Merge Sort).
        Временная сложность: O(n log n) в худшем, среднем и лучшем случаях.
        Сортирует по убыванию веса (сначала самые полезные).
        """
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = cls.merge_sort(arr[:mid])
        right = cls.merge_sort(arr[mid:])

        return cls._merge(left, right)

    @classmethod
    def _merge(cls, left: list, right: list) -> list:
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            # Сравниваем по составному критерию
            if cls._calculate_weight(left[i]) >= cls._calculate_weight(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result
