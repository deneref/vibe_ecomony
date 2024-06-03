from enum import StrEnum


class SheetNames(StrEnum):
    allocatedSpending = 'Аллоцированный расход'
    opEx = 'Операционные расходы'
    capEx = 'Единоразовые расходы'
    supply = 'Размер поставки'
    investments = 'Источники инвестирования'
    result = 'final'  # тестовый sheet
    total_product_cost = 'total_product_cost'  # тестовый
