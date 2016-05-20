# -*- coding: utf-8 -*-
from __future__ import division
from math import ceil
import scrapy
from bs4 import BeautifulSoup as bs
import re
from ScrapyBanksCurrency.items import ScrapybankscurrencyItem as CurrencyItem
import json
from datetime import datetime
from scrapy.utils.response import open_in_browser
from scrapy.shell import inspect_response

with open("./banks.json") as banks_file:
    banks = json.load(banks_file)
    bank_names = [bank for bank in banks.keys()]


bank_from_url = {}
for bank in banks.keys():
    bank_from_url[banks[bank]["url"]] = bank


class CurrenyspiderSpider(scrapy.Spider):

    name = "CurrenySpider"
    start_urls = []
    for bank in bank_names:
        start_urls.append(banks[bank]["url"])
    start_urls = [banks["btk"]["url"]]

    def parse(self, response):
        currency_code = re.compile("[A-Z]{3}")
        unit = re.compile("\A[10]+\Z")
        price = re.compile("\A\d+[.,]{1}\d+\Z")

        bank_name = bank_from_url[response.url]
        try:
            table = bs(response.xpath(banks[bank_name][
                "selector"]).extract()[0], "lxml")
        except:
            inspect_response(response, self)
        rows = [row for row in table.findAll("tr")]
        total_n_cols = 0
        for row in rows:
            total_n_cols += len(row.findAll("td"))
        # If number of columns is less than average, ignore row
        try:
            avg_cols = int(ceil(total_n_cols / len(rows)))
        except:
            inspect_response(response, self)
        for row in rows:
            columns = row.findAll("td")
            print(len(columns), avg_cols)
            if len(columns) < avg_cols:
                continue
            item = CurrencyItem()
            item["bank"] = bank_name
            item["date"] = datetime.today().date()
            for column in columns:
                col_content = column.text.strip()
                if price.match(col_content) is not None:
                    match = float(price.match(
                        col_content).group().replace(",", "."))
                    item["buy_price"] = match
                    try:
                        if match > item["sell_price"]:
                            item["buy_price"] = item["sell_price"]
                            item["sell_price"] = match
                    except KeyError as e:
                        item["sell_price"] = match
                if currency_code.match(col_content) is not None:
                    item["currency_code"] = currency_code.match(
                        col_content).group()
                if unit.match(col_content) is not None:
                    item["unit"] = unit.match(col_content).group()
            yield item
