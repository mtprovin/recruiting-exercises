import unittest
from inventory_allocator import *

class TestCases(unittest.TestCase):

    def testExample1(self):
        order = {"apple": 1}
        warehouses = [{"name": "owd", "inventory": {"apple": 1}}]
        expectedShipment = [{"owd": {"apple": 1}}]
        actualShipment = inventoryAllocator(order, warehouses)
        self.assertEqual(expectedShipment, actualShipment)

    def testExample2(self):
        order = {"apple": 10}
        warehouses = [{"name": "owd", "inventory": {"apple": 5}}, {"name": "dm", "inventory": {"apple": 5}}]
        expectedShipment = [{"owd": {"apple": 5}}, {"dm": {"apple": 5}}]
        actualShipment = inventoryAllocator(order, warehouses)
        self.assertEqual(expectedShipment, actualShipment)

    def testExample3(self):
        order = {"apple": 1}
        warehouses = [{"name": "owd", "inventory": {"apple": 0}}]
        expectedShipment = []
        actualShipment = inventoryAllocator(order, warehouses)
        self.assertEqual(expectedShipment, actualShipment)

    def testExample4(self):
        order = {"apple": 2}
        warehouses = [{"name": "owd", "inventory": {"apple": 1}}]
        expectedShipment = []
        actualShipment = inventoryAllocator(order, warehouses)
        self.assertEqual(expectedShipment, actualShipment)

    def testSplit(self):
        order = {"apple": 10}
        warehouses = [{"name": "owd", "inventory": {"apple": 3}}, {"name": "dm", "inventory": {"apple": 3}},
                      {"name": "amz", "inventory": {"apple": 3}}, {"name": "dxt", "inventory": {"apple": 3}}]
        expectedShipment = [{"owd": {"apple": 3}}, {"dm": {"apple": 3}},
                            {"amz": {"apple": 3}}, {"dxt": {"apple": 1}}]
        actualShipment = inventoryAllocator(order, warehouses)
        self.assertEqual(expectedShipment, actualShipment)

    def testFailOrder1(self):
        order = {"apple": 10, "pear": 3}
        warehouses = [{"name": "owd", "inventory": {"apple": 8}}, {"name": "dm", "inventory": {"apple": 2, "pear": 1}}]
        expectedShipment = []
        actualShipment = inventoryAllocator(order, warehouses)
        self.assertEqual(expectedShipment, actualShipment)

    def testFailOrder2(self):
        order = {"apricot": 1, "lime": 3}
        warehouses = [{"name": "owd", "inventory": {"orange": 8}}, {"name": "dm", "inventory": {"apple": 2, "pear": 1}},
                      {"name": "tx", "inventory": {"bread": 2}}]
        expectedShipment = []
        actualShipment = inventoryAllocator(order, warehouses)
        self.assertEqual(expectedShipment, actualShipment)

    def testCombineSplit1(self):
        order = {"apple": 10}
        warehouses = [{"name": "owd", "inventory": {"apple": 5}}, {"name": "dm", "inventory": {"apple": 5}},
                      {"name": "amz", "inventory": {"apple": 10}}]
        expectedShipment = [{"amz": {"apple": 10}}]
        actualShipment = inventoryAllocator(order, warehouses)
        self.assertEqual(expectedShipment, actualShipment)
    
    def testCombineSplit2(self):
        order = {"apple": 10}
        warehouses = [{"name": "owd", "inventory": {"apple": 3}}, {"name": "dm", "inventory": {"apple": 3}},
                      {"name": "amz", "inventory": {"apple": 3}}, {"name": "dxt", "inventory": {"apple": 20}}]
        expectedShipment = [{"dxt": {"apple": 10}}]
        actualShipment = inventoryAllocator(order, warehouses)
        self.assertEqual(expectedShipment, actualShipment)

    def testCombineSplit3(self):
        order = {"apple": 10, "banana": 2}
        warehouses = [{"name": "owd", "inventory": {"apple": 5}}, {"name": "dm", "inventory": {"apple": 2, "banana": 2}},
                      {"name": "dude", "inventory": {"apple": 3}}, {"name": "amz", "inventory": {"apple": 10}}]
        expectedShipment = [{"dm": {"apple": 2, "banana": 2}}, {"amz": {"apple": 8}}]
        actualShipment = inventoryAllocator(order, warehouses)
        self.assertEqual(expectedShipment, actualShipment)

    def testCombineSplit4(self):
        order = {"apple": 10}
        warehouses = [{"name": "abc", "inventory": {"apple": 3}}, 
                      {"name": "def", "inventory": {"apple": 3}},
                      {"name": "ALL", "inventory": {"apple": 10}},
                      {"name": "ghi", "inventory": {"apple": 3}},
                      {"name": "jkl", "inventory": {"apple": 3}},
                      {"name": "mno", "inventory": {"apple": 3}},
                      {"name": "pqr", "inventory": {"apple": 3}},
                      {"name": "stu", "inventory": {"apple": 3}}]
        expectedShipment = [{"ALL": {"apple": 10}}]
        actualShipment = inventoryAllocator(order, warehouses)
        self.assertEqual(expectedShipment, actualShipment)

    def testLong1(self):
        order = {"milk": 3, "cookie": 12, "egg": 12, "cucumber": 2, "flour": 1, "tomato": 3, "bread": 1, "chicken": 2}
        warehouses = [{"name": "owd", "inventory": {"milk": 12}},                  {"name": "dm", "inventory": {"bread": 1}},
                      {"name": "amz", "inventory": {"flour": 2}},                  {"name": "dxt", "inventory": {"chicken": 17}},
                      {"name": "skip1", "inventory": {"zuccini": 1, "squash": 3}}, {"name": "ra", "inventory": {"tomato": 64}},
                      {"name": "trg", "inventory": {"cookie": 21}},                {"name": "skip2", "inventory": {"rice": 7}},
                      {"name": "sfw", "inventory": {"egg": 48, "cucumber": 9}},    {"name": "skip3", "inventory": {"lettuce": 3}}]
        expectedShipment = [{"owd": {"milk": 3}}, {"dm": {"bread": 1}},
                            {"amz": {"flour": 1}}, {"dxt": {"chicken": 2}},
                            {"ra": {"tomato": 3}}, {"trg": {"cookie": 12}},
                            {"sfw": {"egg": 12, "cucumber": 2}}]
        actualShipment = inventoryAllocator(order, warehouses)
        self.assertEqual(expectedShipment, actualShipment)

    def testLong2(self):
        order = {"chocolate": 1, "sugar": 3, "butter": 4, "raspberry": 1, "starch": 2, "cream": 2, "egg": 3}
        warehouses = [{"name": "skip1", "inventory": {"milk": 12, "pie": 40, "cake": 21, "yogurt": 43, "orange": 90, "cheese": 4, "pudding": 33}},
                      {"name": "bsc", "inventory": {"butter": 1, "spaghetti": 20, "starch": 20, "cream": 70, "cantelope": 4}},
                      {"name": "cre", "inventory": {"flour": 2, "chocolate": 10, "fish": 14, "eggplant": 2, "raspberry": 1, "egg": 2}},
                      {"name": "sb", "inventory": {"chicken": 17, "sugar": 39, "butter": 3, "beef": 8}},
                      {"name": "e", "inventory": {"zuccini": 1, "ice": 2, "egg": 1, "carrot": 13, "walnut": 21, "squash": 3}}]
        expectedShipment = [{"bsc": {"butter": 1, "starch": 2, "cream": 2}},
                            {"cre": {"chocolate": 1, "raspberry": 1, "egg": 2}},
                            {"sb": {"sugar": 3, "butter": 3}},
                            {"e": {"egg": 1}}]
        actualShipment = inventoryAllocator(order, warehouses)
        self.assertEqual(expectedShipment, actualShipment)

if __name__ == "__main__":
    unittest.main()
