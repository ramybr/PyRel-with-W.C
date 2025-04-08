

def define_report():
    from relationalai.std import aggregates, strings
    from bs.model import M
    from bs.model import Customers, Orders, OrderItems
    


    CustomerOrderSummary = M.Type("CustomerOrderSummary")

    with M.rule():
        c = Customers()
        CustomerOrderSummary.add(id=c.id)
    with M.rule():
        c = Customers()
        cos = CustomerOrderSummary()
        cos.set(
            name=strings.concat(c.first_name, " ", c.last_name),
            email=c.email
        )
    
    with M.rule():
        o = Orders()
        cos = CustomerOrderSummary()
        orders = o(customer_id=cos.customer_id)
        cos.set(
            total_orders=aggregates.count(orders),
            last_order_date=aggregates.max(orders.order_date)
        )

    with M.rule():
        cos = CustomerOrderSummary()
        o = Orders(customer_id=cos.customer_id)
        item = OrderItems(order_id=o.id)
        item_value = item.quantity * item.listing_price * (1 - item.discount.or_(0))
        cos.set(
            lifetime_value=aggregates.sum(item_value),
            avg_order_value=aggregates.avg(item_value),
            total_items=aggregates.count(item)
        )

    def report_query():
        cos = CustomerOrderSummary()
        return(
            cos.name,
            cos.email,
            cos.total_orders,
            cos.last_order_date,
            cos.lifetime_value,
            cos.avg_order_value,
            cos.total_items
        )  
    return report_query




        