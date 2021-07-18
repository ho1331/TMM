import pytest
from tests.testfiles import codetotest as code


# test even_odd()
def test_even_odd():
    assert code.even_odd(4) == "even"
    assert code.even_odd(5) == "odd"


# -----------------------------------------------------------------------------------------
# test sum_all()
@pytest.mark.parametrize(
    "args",
    [
        list(range(50)),
        [float(i) for i in range(45)],
        [int(i) + float(x) for i in range(34) for x in range(10)],
    ],
)
def test_sun_all(args):
    assert code.sum_all(*args) == sum(args)


# -----------------------------------------------------------------------------------------

# test class Product
@pytest.fixture
def obj_product():
    return code.Product("apple", 20, 4)


def test_subtract_quantity(obj_product):
    obj_product.subtract_quantity(4)
    assert obj_product.quantity >= 0


def test_add_quantity(obj_product):
    obj_product.quantity = 0
    obj_product.add_quantity()
    assert obj_product.quantity > 0


def test_change_price(obj_product):
    price = obj_product.price
    obj_product.change_price(20.4)
    assert (obj_product.price > price) and (type(obj_product.price) == float)


# -----------------------------------------------------------------------------------------
# test class Shop
@pytest.fixture
def obj_shop():
    return code.Shop()


def test_init(obj_product, obj_shop):
    assert obj_shop.products == []
    # more 1 product
    assert code.Shop([obj_product, obj_product]).products == [obj_product, obj_product]
    # one product
    one_product = code.Product('onion',10)
    assert code.Shop(one_product).products == [one_product]


def test_add_product(obj_product, obj_shop):
    obj_shop.add_product(obj_product)
    assert obj_product in obj_shop.products


def test_get_product_index(obj_product, obj_shop):
    assert obj_shop._get_product_index(obj_product.title) == None
    obj_shop.add_product(obj_product)
    assert obj_shop._get_product_index(obj_product.title) == obj_shop.products.index(
        obj_product
    )


@pytest.fixture
def zero_product():
    return code.Product("banana", 30, 0)


def test_sell_product(obj_product, zero_product):

    # if count of product < qty_to_sell
    shop_obj = code.Shop([zero_product, obj_product])
    with pytest.raises(ValueError):
        shop_obj.sell_product(zero_product.title)

    # if count of product > qty_to_sell
    shop_obj.sell_product(obj_product.title, 1)
    assert obj_product.quantity == 3

    # if count of product == qty_to_sell
    shop_obj.sell_product(obj_product.title, 3)
    assert obj_product not in shop_obj.products

    # check money
    assert shop_obj.money == float(80)



