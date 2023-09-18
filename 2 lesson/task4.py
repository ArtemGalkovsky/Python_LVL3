"""
Класс «Товар» содержит следующие закрытые поля (private):
название товара,
название магазина, в котором продается товар
стоимость товара в рублях
Реализовать геттер (get) и сеттер(set) для доступа к private элементам
"""


class Product:

  def __init__(self) -> None:
    self._product_name: str = ""
    self._shop_name: str = ""
    self._cost: float = 0.0

  @property
  def product_name(self) -> str:
    return self._product_name

  @product_name.setter
  def product_name(self, name: str) -> None:
    self._product_name = name

  @property
  def shop_name(self) -> str:
    return self._shop_name

  @shop_name.setter
  def shop_name(self, name: str) -> None:
    self._shop_name = name

  @property
  def cost(self) -> float:
    return self._cost

  @cost.setter
  def cost(self, cost: float) -> None:
    self._cost = cost


product = Product()

product.product_name = "Pasta"
print("Product name:", product.product_name)

product.shop_name = "Food"
print("Shop name:", product.shop_name)

product.cost = 999.9
print("Cost:", product.cost)
