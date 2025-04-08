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
    cr = Customers
    Customers.add(id=cr.customer_id).set(
        first_name=cr.first_name,
        last_name=cr.last_name,
        phone=cr.phone,
        email=cr.email,
        street=cr.street,
        city=cr.city,
        state=cr.state,
        zip_code=cr.zip_code
    )

with M.rule():
    c = Customers()
    o = Orders()
    Orders.add(id=o.order_id).set(
        customer_id=c.customer_id,
        status=o.order_status,
        order_date=o.order_date,
        required_date=o.required_date,
        shipped_date=o.shipped_date,
        store_id=o.store_id,
        staff_id=o.staff_id
    )

with M.rule():
    p = Products()
    p.add(id=p.product_id).set(
        name=p.product_name,
        brand_id=p.brand_id,
        category_id=p.category_id,
        model_year=p.model_yer,
        listing_price=p.listing_price
    )

with M.rule():
    s = Staff()
    Staff.add(id=s.staff_id).set(
         first_name=s.first_name,
        last_name=s.last_name,
        email=s.email,
        phone=s.email,
        active=s.active,
        store_id=s.store_id,
        manager_id=s.manager_id
    )


with M.rule():
    st = Stores()
    Stores.add(id=st.store_id).set(
         name=st.store_name,
        phone=st.phone,
        email=st.email,
        street=st.street,
        city=st.city,
        state=st.state,
        zip_code=st.zip_code
    )

with M.rule():
    o = Orders()
    oi = OrderItems()
    OrderItems.add(item_id=oi.item_id, order_id=o.id).set(
         product_id=oi.product_id,
        quantity=oi.quantity,
        list_price=oi.list_price,
        discount=oi.discount
    )

with M.rule():
    st = Stores()
    p = Products()
    stc = Stocks()
    Stocks.add(store_id=st.id, product_id=p.id).set(quantity=stc.quantity)

    # I'm not sure if that's the right way to express a join, i couldn't find a clear answer in the docs.