import relationalai as rai
from relationalai.std import aggregates
from relationalai.std.graphs import Graph

provider = rai.Provider()

M = rai.Model("BikeStore", ensure_change_tracking=True)



Brands = M.Type("Brands", source="POV_TEAM.RAMYBR_DD.BRANDS")
Categories = M.Type("Categories", source="POV_TEAM.RAMYBR_DD.CATEGORIES")
Customers = M.Type("Customers", source="POV_TEAM.RAMYBR_DD.CUSTOMERS")
OrderItems = M.Type("OrderItems", source="POV_TEAM.RAMYBR_DD.ORDER_ITEMS")
Orders = M.Type("Orders", source="POV_TEAM.RAMYBR_DD.ORDERS")
Products = M.Type("Products", source="POV_TEAM.RAMYBR_DD.PRODUCTS")
Staff = M.Type("Staffs", source="POV_TEAM.RAMYBR_DD.STAFFS")
Stocks = M.Type("Stocks", source="POV_TEAM.RAMYBR_DD.STOCKS")
Stores = M.Type("Stores", source="POV_TEAM.RAMYBR_DD.STORES")

People = M.Type("People")


with M.rule():
    cst = Customers()
    cst.set(People)

with M.rule():
    stf = Staff()
    stf.set(People)




# using People
# with M.rule():
#     p1 = People()
#     p2 = People()
#     ordr = Orders(customer_id=p1.id, staff_id=p2.id)
#     p1.knows.add(p2)
#     p2.knows.add(p1)


with M.rule():
    cst = Customers()
    stf = Staff()
    ordr = Orders(customer_id=cst.customer_id, staff_id=stf.staff_id)
    cst.knows.add(stf)
    stf.knows.add(cst)

    cst.has_order.add(ordr)


with M.rule():
    prd = Products()
    brnd = Brands(id=prd.brand_id)
    ctg = Categories(id=prd.category_id)

    prd.set(
        has_brand=brnd,
        has_category=ctg
        )

with M.rule():
    ordr = Orders()
    cst = Customers(id=ordr.customer_id)
    st = Stores(id=ordr.store_id)
    stf = Staff(id=ordr.staff_id)
    ordr_itm = OrderItems(order_id=ordr.order_id)

    ordr.set(
        has_customer=cst,
        from_store=st,
        has_staff=stf,
        has_items=ordr_itm #multi-valued should use .add ??
    )


    
with M.rule():
    stc = Stocks() 
    st = Stores(id=stc.store_id)
    pdct = Products(id=stc.product_id)

    stc.set(
        in_store=st,
        has_product=pdct
    )

with M.rule():
    stf = Staff()
    st = Stores(id=stf.store_id)

    stf.set(works_in_store=st)

with M.rule():
    oi = OrderItems()
    ordr = Orders(id=oi.order_id)
    prd = Products(id=oi.product_id)


    oi.set(
        in_order=ordr,
        has_product=prd,
    )

with M.rule():
    ordr = Orders()
    cst = ordr.has_customer
    ordr_itm = ordr.has_items
 

    prd = Products(product_id=ordr_itm.product_id) 
    ordr_itm.set(has_product=prd)

with M.rule():
    ordr = Orders()     
    cat = prd.has_category

    count_categories = aggregates.count(cat.category_name, per=[cat])
    aggregates.rank_desc(count_categories, per=[cst]) == 1

    cst.set(has_favorite_category=cat)