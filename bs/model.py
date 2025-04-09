import relationalai as rai
from relationalai.std import aggregates, top
from relationalai.std.graphs import Graph

provider = rai.Provider()

M = rai.Model("BikeStore", ensure_change_tracking=True)



Brands = M.Type("Brands", source="POV_TEAM.RAMYBR_DT.BRANDS")
Categories = M.Type("Categories", source="POV_TEAM.RAMYBR_DT.CATEGORIES")
Customers = M.Type("Customers", source="POV_TEAM.RAMYBR_DT.CUSTOMERS")
OrderItems = M.Type("OrderItems", source="POV_TEAM.RAMYBR_DT.ORDER_ITEMS")
Orders = M.Type("Orders", source="POV_TEAM.RAMYBR_DT.ORDERS")
Products = M.Type("Products", source="products")
Staff = M.Type("Staffs", source="POV_TEAM.RAMYBR_DT.STAFFS")
Stocks = M.Type("Stocks", source="POV_TEAM.RAMYBR_DT.STOCKS")
Stores = M.Type("Stores", source="POV_TEAM.RAMYBR_DT.SOTRES")

People = M.type("People")

# with M.query() as select:
#     b = Brands()
#     res = select(
#         b.brand_id,
#         b.brand_name
#     )
# print(res.results.head())

# with M.rule():
#     p = People()
#     cst = Customers()
#     stf = Staff()

#     p.customers.add(cst)
#     p.staff.add(stf)


with M.rule():
    cst = Customers()
    cust.set(People)

with M.rule():
    stf = Staff()
    stf.set(People)

# with M.query() as select:
#     p = People()
#     res = select(
#         p.id,
#     )
#     print(res.results.head())


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

with M.rule():
    ordr = Orders() 
    cst = ordr.has_customer
    ordr_itm = OrderItems(order_id=ordr.order_id) # ordr_itm = ordr.has_order_items
    prd = Products(product_id=ordr_itm.product_id) # prd = ordr_itm.has_product
    cat = Categories(category_id=prd.category_id) # cat = prd.has_category
    count_categories = aggregates.count(cat.category_name, per=[cat])
    rank_des(count_categories, per=[cst]) == 1
    # fav_cat = top(1, count_categories)
    # cst.has_favorite_category.set(cat)  Commented cus wrong
    cst.set(has_favorite_category=cat)

with M.rule():
    prd = Products()
    brnd = Brands(id=prd.brand_id)
    ctg = Categories(id=prd.category_id)

    prd.has_brand.set(brnd)
    prd.has_category.set(ctg)

with M.rule():
    ordr = Orders()
    cst = Customers(id=ordr.customer_id)
    st = Stores(id=ordr.store_id)
    stf = Staff(id=ordr.staff_id)

    ordr.has_customer.set(cst)
    ordr.from_store.set(st)
    ordr.has_staff.set(stf)

    
with M.rule():
    stc = Stocks() 
    st = Stores(id=stc.store_id)
    pdct = Products(id=stc.product_id)

    stc.in_store.set(st)
    stc.has_product.set(pdct)

with M.rule():
    stf = Staff()
    st = Stores(id=stf.store_id)

    stf.works_in_store.set(st)

with M.rule():
    oi = OrderItems()
    ordr = Orders(id=oi.order_id)
    prd = Products(id=oi.product_id)

    oi.in_order.set(ordr)
    oi.has_product.set(prd)
