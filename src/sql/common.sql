update today_all set pick = 0 where name like 'ST%' or name like '*ST%' or open = 0 or trade > 20 or nmc > 1000000 or amount < 10000000