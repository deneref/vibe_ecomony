from enum import StrEnum


class SheetNames(StrEnum):
    totalSpending = 'Общий расход'
    opEx = 'Затраты'  # операционные расходы
    capEx = 'Единоразовые расходы'
    supply = 'Размер поставки'
    investments = 'Источники инвестирования'
