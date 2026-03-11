from kaipanla_crawler import KaipanlaCrawler

c = KaipanlaCrawler()
d = c.get_sector_bidding_anomaly()
print(f"日期: {d['date']}, 总数: {d['total_count']}, 今日新增: {len(d['list1'])}, 昨日延续: {len(d['list2'])}")
