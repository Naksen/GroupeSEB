1) Выведите список брендов (Brand), которые продаются в Глобусе (ChainName)

```sql
SELECT DISTINCT DP.Brand
FROM Sales AS S
JOIN DIM_Shops AS DS ON S.IDShop = DS.IDShop
JOIN DIM_Products AS DP ON S.IDSku = DP.IDSku
WHERE DS.ChainName = 'Глобус';
```

2) Посчитайте сумму продаж в гипермаркете METRO (ChainName) за февраль 2021 (Quantity и Amount)

```sql
SELECT SUM(S.Quantity) AS TotalQuantity, SUM(S.Amount) AS TotalAmount
FROM Sales AS S
JOIN DIM_Shops AS DS ON S.IDShop = DS.IDShop
WHERE DS.ChainName = 'METRO' AND YEAR(S.Date) = 2021 AND MONTH(S.Date) = 2;
```

3) Посчитайте кол-во магазинов Эльдорадо (ChainName), по которым были продажи 12/02/2021

```sql
SELECT COUNT(DISTINCT DS.IDShop) AS EldoradoStoreCount
FROM Sales AS S
JOIN DIM_Shops AS DS ON S.IDShop = DS.IDShop
WHERE DS.ChainName = 'Эльдорадо' AND S.Date = '2021-02-12';
```

4) Выведите 5 самых продаваемых товаров (код товара и название) в ДНС (ChainName)

```sql
SELECT TOP 5 S.IDSku AS ProductId, DP.SkuName AS ProductName
FROM Sales AS S
JOIN DIM_Shops AS DS ON S.IDShop = DS.IDShop
JOIN DIM_Products AS DP ON S.IDSku = DP.IDSku
WHERE DS.ChainName = 'ДНС'
GROUP BY S.IDSku, DP.SkuName
ORDER BY SUM(S.Quantity) DESC;
```