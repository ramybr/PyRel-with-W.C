

# def define_report():
from relationalai.std import aggregates, strings
from model import M
from model import Customers, Orders, OrderItems
    


CustomerOrderSummary = M.Type("CustomerOrderSummary")

with M.rule():
        c = Customers()
        CustomerOrderSummary.add(id=c)

with M.rule():
        c = Customers()
        cos = CustomerOrderSummary()
        cos.set(
            name=strings.concat(cos.id.first_name, " ", cos.id.last_name),
            email=cos.id.email
        )

    
with M.rule():
        cos = CustomerOrderSummary()
        cst = Customers()
        orders = cst.has_order
        cos.set(
            total_orders=aggregates.count(orders),
            last_order_date=aggregates.max(orders.order_date)
        )

with M.rule():
        cos = CustomerOrderSummary()
        ordr = Orders()
        item = ordr.has_items
        item_value = item.quantity * item.list_price * (1 - item.discount.or_(0))
        cos.set(
            lifetime_value=aggregates.sum(item_value),
            avg_order_value=aggregates.avg(item_value),
            total_items=aggregates.count(item)
        )

with M.query(format="snowpark") as select:
        cos = CustomerOrderSummary()
        response = select(
            cos.name,
            cos.email,
            cos.total_orders,
            cos.last_order_date,
            cos.lifetime_value,
            cos.avg_order_value,
            cos.total_items
        )  
    
# response.results.write.mode("overwrite").save_as_table("pov_team.ramybr_dd.customer_order_summary")
response.results.show()





        