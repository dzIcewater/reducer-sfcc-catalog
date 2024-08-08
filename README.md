# reducer-sfcc-catalog

Project status:
  In progress

Purpose:
  Reduces a master catalog's size for very large master catalogs. Utilizes site catalogs, pricebooks, inventory xml

Introduction 

  The main motivation for this package is that in SFCC sandboxes we need to have 300 products or less, or else the server slows down to unbearable speeds. 
Therefore this package reduces a master catalog's file size, with consideration of inventory , pricebooks and the site catalog.
Parsing occurs across these files multiple times as needed.

Desired Catalog outcome:
- <= 300 products, including master products with only 2 or 3 variation products assigned.
- Only online products.
- Only products with prices assigned (if variant).
- Only products assigned to the site catalog.




