# -*- coding: utf-8 -*-
import unittest

from gilded_rose import NewItem, Item, GildedRose
from gilded_rose import MAX_QUALITY, LEGENDARY_QUALITY


class NewItemTest(unittest.TestCase):

    def gen_item(self, sell_in=0, quality=80):

        return NewItem(Item("foo", sell_in, quality))

    def gen_legendary(self, sell_in=0, quality=80):

        return NewItem(Item("Sulfuras, Hand of Ragnaros", sell_in, quality))

    def gen_conjured(self, sell_in=0, quality=80):

        return NewItem(Item("Conjured item", sell_in, quality))

    def gen_aged_brie(self, sell_in=0, quality=80):

        return NewItem(Item("Aged Brie", sell_in, quality))

    def gen_backstage_passes(self, sell_in=0, quality=80):

        return NewItem(Item("Backstage passes", sell_in, quality))

    def test_fix_quality(self):
        # fix_quality will be called on init method
        self.assertEqual(MAX_QUALITY, self.gen_aged_brie(0, MAX_QUALITY+10).quality)    
        self.assertEqual(0, self.gen_item(0, -1).quality)   
        self.assertEqual(LEGENDARY_QUALITY, self.gen_legendary(quality=LEGENDARY_QUALITY+10).quality) 

    def test_quality_change_by_day(self):

        self.assertEqual(-1, self.gen_item().quality_change_by_day)
        self.assertEqual(-2, self.gen_conjured().quality_change_by_day)
        self.assertEqual(1, self.gen_aged_brie().quality_change_by_day)

    def test_compute_quality_delta_sell_in_negative(self):

        self.assertEqual(self.gen_item(0).compute_quality_delta * 2, self.gen_item(-1).compute_quality_delta)   

    def test_legendaty_inmutable(self):

        item = self.gen_legendary()
        orig_sell_in = item.sell_in
        orig_quality = item.quality
        item.handle_new_day()
        self.assertEqual(orig_sell_in, item.sell_in)
        self.assertEqual(orig_quality, item.quality)

    def test_handle_new_day(self):

        item = self.gen_item(1, 3)
        item.handle_new_day()
        self.assertEqual(0, item.sell_in)
        self.assertEqual(2, item.quality)    
        item.handle_new_day()
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(0, item.quality) 
        item.handle_new_day()
        self.assertEqual(0, item.quality) 

    def test_conjured(self):

        item = self.gen_conjured(1, 3)
        item.handle_new_day()
        self.assertEqual(1, item.quality)    
        item.handle_new_day()
        self.assertEqual(0, item.quality) 

    def test_aged_brie(self):

        item = self.gen_aged_brie(1, 46)
        item.handle_new_day()
        self.assertEqual(47, item.quality)    
        item.handle_new_day()
        self.assertEqual(49, item.quality) 
        item.handle_new_day()
        self.assertEqual(50, item.quality)   

    def test_backstage_passes(self):
        # check intervals
        self.assertEqual(1, self.gen_backstage_passes(10).compute_quality_delta)  
        self.assertEqual(2, self.gen_backstage_passes(9).compute_quality_delta)    
        self.assertEqual(2, self.gen_backstage_passes(5).compute_quality_delta)  
        self.assertEqual(3, self.gen_backstage_passes(4).compute_quality_delta)
        self.assertEqual(3, self.gen_backstage_passes(0).compute_quality_delta) 
        self.assertEqual(-MAX_QUALITY, self.gen_backstage_passes(-1).compute_quality_delta)  


class GildedRoseTest(unittest.TestCase):

    def test_foo(self):
        items = [Item("foo", 0, 1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("foo", items[0].name)
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(0, items[0].quality)

if __name__ == '__main__':
    unittest.main()

