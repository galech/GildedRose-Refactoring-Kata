# -*- coding: utf-8 -*-


MAX_QUALITY = 50  # except for legendary items
LEGENDARY_QUALITY = 80


class NewItem:

    legendary = False
    quality_change_by_day = -1  # base quality change by day
    custom_intervals = None

    def __init__(self, base_item):

        self.base_item = base_item
        self.legendary = base_item.name == "Sulfuras, Hand of Ragnaros"

        if base_item.name == "Aged Brie":
            self.quality_change_by_day *= -1  # inverse the logic ;)

        if base_item.name.startswith("Conjured"):
            self.quality_change_by_day *= 2  

        if base_item.name.startswith("Backstage passes"):
            self.custom_intervals = [
                {"lte": -1, "change": -MAX_QUALITY},  # need quality to be fixed
                {"interval": [0, 4], "change": 3},
                {"interval": [5, 9], "change": 2},
                {"gte": 10, "change": 1}
            ]

        self.fix_quality()

    @property
    def quality(self):

        return self.base_item.quality

    @property
    def sell_in(self):

        return self.base_item.sell_in

    @property
    def delta_by_interval(self):

        for i_dict in self.custom_intervals:
            if "lte" in i_dict and self.sell_in <= i_dict["lte"]:
                return i_dict["change"]
            if "gte" in i_dict and self.sell_in >= i_dict["gte"]:
                return i_dict["change"]
            if "interval" in i_dict and (i_dict["interval"][0] <= self.sell_in <= i_dict["interval"][1]):
                return i_dict["change"]

        return 1

    @property
    def compute_quality_delta(self):

        if self.custom_intervals:  # custom case
            return self.delta_by_interval
        else:  # normal case
            return self.quality_change_by_day * (2 if self.sell_in < 0 else 1)

    def fix_quality(self):

        if self.legendary:  
            self.base_item.quality = LEGENDARY_QUALITY
        else:
            self.base_item.quality = max(0, min(MAX_QUALITY, self.quality))


    def handle_new_day(self):

        if not self.legendary:

            self.base_item.sell_in -= 1
            self.base_item.quality += self.compute_quality_delta
            self.fix_quality()


class GildedRose(object):

    def __init__(self, items):

        self.items = [NewItem(item) for item in items]

    def update_quality(self):

        for item in self.items:
            item.handle_new_day()


class Item:

    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
