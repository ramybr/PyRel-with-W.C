import relationalai as rai
from relationalai.std import aggregates
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



with M.rule():
    b = Brands()
    Brands.add(id=b.brand_id).set(name=b.brand_name)

with M.rule():
    c = Categories()
    Categories.add(id=c.category_id).set(name=c.category_name)





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