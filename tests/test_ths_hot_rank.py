# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from kaipanla_crawler import KaipanlaCrawler
import pandas as pd


def test_ths_hot_rank():
    print('=' * 60)
    print('Testing THS Hot Rank (20 stocks)')
    print('=' * 60)

    crawler = KaipanlaCrawler()
    print('
Fetching THS hot rank data...')
    print('Note: This requires selenium and chromedriver')

    series = crawler.get_ths_hot_rank(headless=False, wait_time=5)

    if series.empty:
        print('Failed: Empty data returned')
        return False

    print('Success!')
    print(f'
Data count: {len(series)}')
    print(f'Series name: {series.name}')
    print(f'Index name: {series.index.name}')

    print('
' + '=' * 60)
    print('Data preview:')
    print('=' * 60)
    print(series.to_string())

    output_file = 'ths_hot_rank.csv'
    series.to_csv(output_file, encoding='utf-8-sig')
    print(f'
Data saved to: {output_file}')

    return True


if __name__ == '__main__':
    try:
        success = test_ths_hot_rank()
        if success:
            print('
' + '=' * 60)
            print('Test completed!')
            print('=' * 60)
    except Exception as e:
        print(f'
Test exception: {str(e)}')
        import traceback
        traceback.print_exc()
