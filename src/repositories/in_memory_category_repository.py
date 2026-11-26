from datetime import datetime, timezone

from models.complaint_category import ComplaintCategory
from repositories.category_repository import CategoryRepository


class InMemoryCategoryRepository(CategoryRepository):

    def __init__(self):
        self.categories = {}

    def save(self, category: ComplaintCategory) -> ComplaintCategory:
        self.categories[category.id] = category
        return category

    def find_by_id(self, category_id: str) -> ComplaintCategory | None:
        return self.categories.get(category_id)

    def find_by_name(self, name: str) -> ComplaintCategory | None:
        # Case-insensitive comparison
        wanted = name.strip().lower()
        for category in self.categories.values():
            if category.name.lower() == wanted:
                return category
        return None

    def find_all(self) -> list[ComplaintCategory]:
        return list(self.categories.values())

    def update(self, category: ComplaintCategory) -> ComplaintCategory | None:
        if category.id not in self.categories:
            return None
        self.categories[category.id] = category
        return category

    def deactivate(self, category_id: str) -> ComplaintCategory | None:
        category = self.find_by_id(category_id)
        if category is None:
            return None
        category.is_active = False
        category.updated_at = datetime.now(timezone.utc)
        return self.update(category)