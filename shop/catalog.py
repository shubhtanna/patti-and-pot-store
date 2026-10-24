"""The shop's range, loaded into the database by migration 0002."""

CATEGORIES = [
    ("assam", "Assam", "Bold, malty black teas from the Brahmaputra valley", 1),
    ("darjeeling", "Darjeeling", "Light, floral teas from the Himalayan foothills", 2),
    ("nilgiri", "Nilgiri", "Bright, brisk teas from the Blue Mountains", 3),
    ("chai-blends", "Chai & blends", "Masala chai and herbal infusions", 4),
    ("teaware", "Teaware", "Kettles, cups and strainers", 5),
]

# sku, slug, name, category, region, weight, price, mrp, stock, notes, brew, description, colour, featured
PRODUCTS = [
    ("PP-AS-01", "assam-breakfast-ctc", "Assam Breakfast CTC", "assam", "Dibrugarh, Assam", "250 g", 249, 299, 60,
     "Malty, strong, coppery cup", "2 tsp · boil with milk · 4 min", "Our everyday kadak chai tea. Strong enough for milk and sugar, granular CTC that brews fast.", "#8b2e16", True),
    ("PP-AS-02", "halmari-gold-assam", "Halmari Gold Assam", "assam", "Halmari Estate, Assam", "100 g", 549, 649, 18,
     "Honeyed malt, golden tips", "1 tsp · 95°C · 4 min", "Whole-leaf second-flush Assam studded with golden tips. Rich enough to drink without milk.", "#b8860b", True),
    ("PP-AS-03", "assam-orthodox-tgfop", "Assam Orthodox TGFOP", "assam", "Upper Assam", "250 g", 399, 449, 32,
     "Brisk, malty, a little spice", "1 tsp · 95°C · 3–4 min", "A classic orthodox leaf for a proper pot of breakfast tea.", "#7a3b1d", False),
    ("PP-AS-04", "assam-masala-ctc-1kg", "Assam CTC Value Pack (1 kg)", "assam", "Assam", "1 kg", 699, 849, 25,
     "Strong, full-bodied", "2 tsp · boil with milk · 4 min", "The breakfast CTC in a kilo pack for big families and offices.", "#5b2410", False),

    ("PP-DJ-01", "darjeeling-first-flush", "Darjeeling First Flush", "darjeeling", "Castleton, Darjeeling", "100 g", 649, 799, 14,
     "Floral, green, muscatel hints", "1 tsp · 85°C · 3 min", "The spring harvest: light, bright and fragrant. Drink it without milk.", "#5f7d3a", True),
    ("PP-DJ-02", "darjeeling-second-flush-muscatel", "Darjeeling Second Flush Muscatel", "darjeeling", "Margaret's Hope, Darjeeling", "100 g", 799, 949, 9,
     "Muscatel grape, ripe fruit", "1 tsp · 90°C · 3–4 min", "The famous summer flush with the muscatel character Darjeeling is known for.", "#7b3f61", False),
    ("PP-DJ-03", "darjeeling-everyday", "Darjeeling Everyday", "darjeeling", "Darjeeling", "250 g", 449, 549, 28,
     "Light, smooth, floral", "1 tsp · 90°C · 3 min", "An approachable Darjeeling blend for daily drinking. A gentle start to the morning.", "#3f7f6f", False),
    ("PP-DJ-04", "darjeeling-autumn-flush", "Darjeeling Autumn Flush", "darjeeling", "Glenburn, Darjeeling", "100 g", 549, 649, 0,
     "Woody, mellow, coppery", "1 tsp · 90°C · 4 min", "Autumn leaves make a rounder, woodier cup. Back in stock after the Puja season.", "#9a5b2c", False),

    ("PP-NG-01", "nilgiri-frost-tea", "Nilgiri Frost Tea", "nilgiri", "Korakundah, Nilgiris", "100 g", 499, 599, 12,
     "Citrus, crisp, clean", "1 tsp · 90°C · 3 min", "Harvested in winter frost season for an unusually bright and clean cup.", "#2f5f8a", False),
    ("PP-NG-02", "nilgiri-black-orthodox", "Nilgiri Black Orthodox", "nilgiri", "Coonoor, Nilgiris", "250 g", 349, 399, 30,
     "Brisk, fragrant", "1 tsp · 95°C · 3 min", "A fragrant, brisk black tea that also makes a great iced tea.", "#264d6e", False),

    ("PP-CB-01", "masala-chai-blend", "Masala Chai Blend", "chai-blends", "Blended in Pune", "250 g", 299, 349, 55,
     "Cardamom, ginger, clove, cinnamon", "2 tsp · boil with milk · 5 min", "Assam CTC with whole spices, freshly ground. Just add milk and sugar.", "#a8432a", True),
    ("PP-CB-02", "kashmiri-kahwa", "Kashmiri Kahwa", "chai-blends", "Blended in Pune", "100 g", 399, 449, 20,
     "Saffron, cardamom, almond", "1 tsp · 90°C · 4 min", "Green tea with saffron, cardamom and cinnamon. Serve with crushed almonds.", "#c48a1b", False),
    ("PP-CB-03", "tulsi-green-tea", "Tulsi Green Tea", "chai-blends", "Blended in Pune", "100 g", 249, 299, 26,
     "Fresh, herbal, calming", "1 tsp · 80°C · 3 min", "Nilgiri green tea with Rama and Krishna tulsi.", "#4f7a3a", False),

    ("PP-TW-01", "glass-teapot-infuser", "Glass Teapot with Infuser (600 ml)", "teaware", "", "600 ml", 899, 1099, 15,
     "", "", "Borosilicate glass pot with a steel infuser. Watch the leaves unfurl.", "#6c7a89", False),
    ("PP-TW-02", "kulhad-set-of-6", "Terracotta Kulhad Set (6)", "teaware", "", "Set of 6, 120 ml", 349, 399, 40,
     "", "", "Hand-thrown clay cups that give chai its earthy roadside-stall taste.", "#b5653c", True),
    ("PP-TW-03", "steel-tea-strainer", "Stainless Steel Tea Strainer", "teaware", "", "Fine mesh, 8 cm", 149, 199, 70,
     "", "", "A fine double mesh that catches even CTC dust.", "#8d99a6", False),
]
