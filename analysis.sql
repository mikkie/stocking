select date,dif,dea FROM stocking.hist where ABS(ROUND(dif, 4) - ROUND(dea, 4)) < 0.00125