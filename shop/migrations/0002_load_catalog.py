from django.db import migrations


def load(apps, schema_editor):
    from shop.catalog import CATEGORIES, PRODUCTS

    Category = apps.get_model("shop", "Category")
    Product = apps.get_model("shop", "Product")
    cats = {}
    for slug, name, blurb, position in CATEGORIES:
        cats[slug], _ = Category.objects.update_or_create(slug=slug, defaults={"name": name, "blurb": blurb, "position": position})
    for i, (sku, slug, name, cat, region, weight, price, mrp, stock, notes, brew, desc, colour, featured) in enumerate(PRODUCTS):
        Product.objects.update_or_create(sku=sku, defaults=dict(
            slug=slug, name=name, category=cats[cat], region=region, weight=weight, price=price, mrp=mrp, stock=stock,
            tasting_notes=notes, brew=brew, description=desc, colour=colour, featured=featured, position=i))


class Migration(migrations.Migration):
    dependencies = [("shop", "0001_initial")]
    operations = [migrations.RunPython(load, migrations.RunPython.noop)]
