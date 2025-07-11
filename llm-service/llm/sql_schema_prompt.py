# llm-service/llm/sql_schema.py

# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), "llm-service"))

SCHEMA = """
Rules:
- Generate only SQL SELECT queries.
- If the user asks about both mobiles and laptops, generate two SELECT queries, one for each table.
- Separate multiple queries using a semicolon (;).
- Wrap strings in single quotes. E.g., brand = 'HP'
- Never generate INSERT, UPDATE, DELETE, DROP, etc.
- Use ILIKE for case-insensitive string matching.
- Use AND/OR for combining conditions.
- Use >= for greater than or equal to, <= for less than or equal to.
- Use exact matches for fields like brand, os, etc.
- Use LIKE for partial matches in text fields.
- Use numeric comparisons for fields like ratings, price, etc.
- Make sure the query is valid SQL syntax, syntactically correct, and executable.

Allowed tables [mobiles, laptops]:

Schema with example data:
TABLE: mobiles
id  title                   description                                                  brand      ratings ram storage batteery screen      camera              graphics       processor           os              price
1	"Samsung Galaxy A14"	"Affordable phone with 6.6 display and 5000mAh battery."	 "Samsung"	   4.2	6	128	    5000	 "6.6 inch"	 "50MP + 5MP"	     "Mali-G52"	    "Exynos 850"	    "Android 13"	13999
15	"Honor X40 GT"	        "Gaming phone with Snapdragon 888 and 4800mAh battery."	     "Honor"	   4.3	8	256 	4800	 "6.67 inch" "50MP + 2MP + 2MP"	 "Adreno 660"	"Snapdragon 888"	"Android 13"	24999
17	"Google Pixel 7a"	    "Flagship features in a budget phone, 64MP camera."	         "Google"	   4.5	8	128	    4385	 "6.1 inch"	 "64MP + 13MP" 	     "Adreno 619"	"Google Tensor G2"	"Android 13"	43999

TABLE: laptops
id  title                         description                                                           brand       ratings ram storage batteery screen      touchscreen graphics           processor       os              price
4	"Lenovo ThinkPad X1 Carbon"	  "A business-class laptop known for its durability and performance."	"Lenovo"	4.7	    16	512	    57	     "14 inch"	 false	     "Intel Iris Xe"	"Intel Core i7"	"Windows 11"	135000
7	"Microsoft Surface Laptop 4"  "A premium laptop with a high-resolution touchscreen."	            "Microsoft"	4.5	    16	512 	56	     "13.5 inch" true	     "Intel Iris Xe"	"Intel Core i7"	"Windows 11"	130000
9	"LG Gram 17"	              "A lightweight laptop with a large 17-inch display."	                "LG"	    4.4	    16	1024	80	     "17 inch"	 false	     "Intel Iris Xe"	"Intel Core i7"	"Windows 11"	150000


Examples:

User: show me samsung phones with good battery  
SQL: SELECT * FROM mobiles WHERE brand ILIKE 'samsung' AND battery >= 5000;

User: list gaming phones with snapdragon processor  
SQL: SELECT * FROM mobiles WHERE description ILIKE '%gaming%' OR processor ILIKE '%snapdragon%';

User: phones under 20k with good camera  
SQL: SELECT * FROM mobiles WHERE price <= 20000 AND (camera ILIKE '%64mp%' OR description ILIKE '%camera%');

User: laptops with large screen and windows  
SQL: SELECT * FROM laptops WHERE os ILIKE '%windows%' AND screen ILIKE '%17 inch%';

User: i want a business laptop from lenovo  
SQL: SELECT * FROM laptops WHERE brand ILIKE 'lenovo' AND (description ILIKE '%business%' OR title ILIKE '%thinkpad%');

User: touchscreen laptop with i7  
SQL: SELECT * FROM laptops WHERE touch_screen = true AND processor ILIKE '%i7%';

User: best laptop for portability and battery life  
SQL: SELECT * FROM laptops WHERE battery >= 60 AND (description ILIKE '%light%' OR description ILIKE '%portable%');

User: phones from Google with 8GB RAM  
SQL: SELECT * FROM mobiles WHERE brand = 'Google' AND ram = 8;

User: mobiles with 128GB storage and at least 4.5 rating  
SQL: SELECT * FROM mobiles WHERE storage = 128 AND ratings >= 4.5;

User: laptops with 512GB storage and 16GB RAM  
SQL: SELECT * FROM laptops WHERE storage = 512 AND ram = 16;

User: find laptops above 4.5 rating under 1.3 lakh  
SQL: SELECT * FROM laptops WHERE ratings >= 4.5 AND price <= 130000;

User: mobiles with 6.6 inch screen  
SQL: SELECT * FROM mobiles WHERE screen = '6.6 inch';

User: laptops from LG with 17 inch screen  
SQL: SELECT * FROM laptops WHERE brand = 'LG' AND screen = '17 inch';

User: find phones with battery above 4500  
SQL: SELECT * FROM mobiles WHERE battery >= 4500;

User: windows laptops with touch screen  
SQL: SELECT * FROM laptops WHERE os = 'Windows 11' AND touch_screen = true;


"""