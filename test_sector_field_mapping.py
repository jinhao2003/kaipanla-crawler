"""测试板块数据字段映射"""

import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from kaipanla_crawler import KaipanlaCrawler


def test_sector_field_mapping():
    """测试板块数据字段映射"""
    print("=" * 60)
    print("测试板块数据字段映射")
    print("=" * 60)
    
    crawler = KaipanlaCrawler()
    
    try:
        # 获取板块数据
        sector_data = crawler.get_sector_ranking("2026-01-16", timeout=60)
        
        if 'sectors' in sector_data and sector_data['sectors']:
            first_sector = sector_data['sectors'][0]
            print(f"\n第一个板块: {first_sector['sector_name']}")
            
            if first_sector['stocks']:
                print(f"\n显示前3只股票的所有字段:")
                
                for stock_idx, stock in enumerate(first_sector['stocks'][:3], 1):
                    print(f"\n  股票 {stock_idx}:")
                    for key, value in stock.items():
                        value_str = str(value)
                        if len(value_str) > 80:
                            value_str = value_str[:80] + "..."
                        print(f"    {key}: {value_str}")
                
                # 分析字段内容
                print(f"\n\n字段内容分析:")
                first_stock = first_sector['stocks'][0]
                
                print(f"\n1. 基本信息:")
                print(f"   股票代码: {first_stock.get('股票代码', '')}")
                print(f"   股票名称: {first_stock.get('股票名称', '')}")
                
                print(f"\n2. 连板信息:")
                print(f"   连板天数: {first_stock.get('连板天数', '')}")
                print(f"   连板描述: {first_stock.get('连板描述', '')}")
                print(f"   连板次数: {first_stock.get('连板次数', '')}")
                
                print(f"\n3. 题材信息:")
                print(f"   概念标签: {first_stock.get('概念标签', '')}")
                print(f"   主题: {first_stock.get('主题', '')[:100] if first_stock.get('主题', '') else ''}...")
                print(f"   涨停原因: {first_stock.get('涨停原因', '')}")
                
                print(f"\n4. 其他信息:")
                print(f"   主力资金: {first_stock.get('主力资金', '')}")
                print(f"   是否首板: {first_stock.get('是否首板', '')}")
                
                # 检查字段是否错位
                print(f"\n\n字段错位检查:")
                print(f"  连板天数字段值: '{first_stock.get('连板天数', '')}'")
                print(f"    - 是否包含'连板'文字: {'连板' in str(first_stock.get('连板天数', ''))}")
                print(f"    - 是否是数字: {isinstance(first_stock.get('连板天数', ''), (int, float))}")
                
                print(f"\n  主题字段值长度: {len(str(first_stock.get('主题', '')))}")
                print(f"    - 是否是长文本(>50字符): {len(str(first_stock.get('主题', ''))) > 50}")
                
                print(f"\n  涨停原因字段值: '{first_stock.get('涨停原因', '')}'")
                print(f"    - 是否是长文本(>50字符): {len(str(first_stock.get('涨停原因', ''))) > 50}")
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_sector_field_mapping()
