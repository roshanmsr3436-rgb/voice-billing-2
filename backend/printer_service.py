from escpos.printer import Network, Usb, Serial, Dummy
import datetime

class PrinterService:
    def __init__(self, printer_name="Dummy"):
        self.printer_name = printer_name
        
    def get_printer(self):
        # Fallback to Dummy printer if actual printer is not available
        try:
            # Example USB configuration (vendor_id, product_id)
            # return Usb(0x04b8, 0x0202, 0, 0x81, 0x03)
            return Dummy()
        except Exception as e:
            print(f"Printer error: {e}")
            return Dummy()

    def print_bill(self, bill, items, settings):
        p = self.get_printer()
        
        shop_name = settings.get('shop_name', 'VOICEBILL TAMIL')
        
        p.set(align='center', font='a', width=2, height=2)
        p.text(f"{shop_name}\n")
        p.set(align='center', font='a', width=1, height=1)
        p.text("================================\n")
        
        p.set(align='left')
        p.text(f"Bill No: {bill['bill_number']}\n")
        p.text(f"Date: {bill['created_at']}\n")
        p.text("--------------------------------\n")
        p.text("ITEM       QTY    PRICE    TOTAL\n")
        p.text("--------------------------------\n")
        
        for item in items:
            name = item['name'][:10].ljust(10)
            qty = f"{item['quantity']}{item['unit']}".ljust(6)
            price = str(item['price']).rjust(5)
            total = str(item['total']).rjust(7)
            p.text(f"{name} {qty} {price} {total}\n")
            
        p.text("--------------------------------\n")
        p.set(align='right')
        p.text(f"Subtotal: Rs.{bill['subtotal']}\n")
        p.text(f"GST: Rs.{bill['gst']}\n")
        p.text(f"Discount: Rs.{bill['discount']}\n")
        p.text("--------------------------------\n")
        p.set(align='right', font='a', width=2, height=2)
        p.text(f"TOTAL: Rs.{bill['grand_total']}\n")
        
        p.set(align='center', font='a', width=1, height=1)
        p.text("================================\n")
        p.text("THANK YOU\nVISIT AGAIN\n\n\n\n")
        
        p.cut()
        
        # If dummy, print to console
        if isinstance(p, Dummy):
            print(p.output.decode('utf-8'))
        
        return True
