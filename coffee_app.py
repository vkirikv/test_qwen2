"""
Specialty Coffee E-Commerce App using Kivy
Features: 6 sample products, search, category filters, product details, 
          cart controls, quantity updates, and simulated checkout.
Optimized for mobile support.
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window

# Set window size for mobile-like experience
Window.size = (360, 640)

# KV Design Language
KV = '''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

ScreenManager:
    transition: FadeTransition()
    MainScreen:
    ProductDetailScreen:
    CartScreen:
    CheckoutScreen:
    CheckoutSuccessScreen:

<MainScreen>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'
        
        # Header
        BoxLayout:
            size_hint_y: None
            height: dp(60)
            padding: dp(10)
            spacing: dp(10)
            
            MDBoxLayout:
                orientation: 'vertical'
                
                Label:
                    text: '☕ Specialty Coffee'
                    font_size: dp(20)
                    bold: True
                    halign: 'left'
                    size_hint_y: None
                    height: dp(30)
                
                Label:
                    text: 'Premium beans from around the world'
                    font_size: dp(12)
                    halign: 'left'
                    size_hint_y: None
                    height: dp(25)
            
            Widget:
            
            BoxLayout:
                size_hint_x: None
                width: dp(80)
                spacing: dp(5)
                orientation: 'vertical'
                
                Button:
                    text: f'🛒 ({app.cart_count})'
                    size_hint: 1, 0.5
                    on_release: app.root.current = 'cart'
                
                Button:
                    text: '🔍'
                    size_hint: 1, 0.5
                    on_release: root.toggle_search()
        
        # Search Bar (collapsible)
        BoxLayout:
            id: search_container
            size_hint_y: None
            height: dp(0)
            padding: dp(10)
            spacing: dp(10)
            
            TextInput:
                id: search_input
                hint_text: 'Search coffee...'
                multiline: False
                on_text: root.filter_products(self.text)
            
            Button:
                text: '✕'
                size_hint_x: None
                width: dp(40)
                on_release: 
                    root.clear_search()
                    root.toggle_search()
        
        # Category Filters
        ScrollView:
            size_hint_y: None
            height: dp(50)
            
            BoxLayout:
                id: category_filters
                size_hint_x: None
                width: self.minimum_width
                padding: dp(10)
                spacing: dp(10)
                
                ToggleButton:
                    text: 'All'
                    group: 'category'
                    active: True
                    on_release: root.filter_by_category('all')
                
                ToggleButton:
                    text: 'Espresso'
                    group: 'category'
                    on_release: root.filter_by_category('espresso')
                
                ToggleButton:
                    text: 'Single Origin'
                    group: 'category'
                    on_release: root.filter_by_category('single_origin')
                
                ToggleButton:
                    text: 'Blend'
                    group: 'category'
                    on_release: root.filter_by_category('blend')
                
                ToggleButton:
                    text: 'Decaf'
                    group: 'category'
                    on_release: root.filter_by_category('decaf')
        
        # Products Grid
        ScrollView:
            GridLayout:
                id: products_grid
                cols: 2
                size_hint_y: None
                height: self.minimum_height
                padding: dp(10)
                spacing: dp(10)
                
                # Products will be added dynamically
        
        # Bottom Navigation
        BoxLayout:
            size_hint_y: None
            height: dp(60)
            padding: dp(10)
            spacing: dp(10)
            
            Button:
                text: '🏠 Home'
                on_release: app.root.current = 'main'
            
            Button:
                text: f'🛒 Cart ({app.cart_count})'
                on_release: app.root.current = 'cart'

<ProductDetailScreen>:
    name: 'detail'
    BoxLayout:
        orientation: 'vertical'
        
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            padding: dp(10)
            
            Button:
                text: '← Back'
                on_release: app.root.current = 'main'
            
            Label:
                text: 'Product Details'
                font_size: dp(18)
                bold: True
        
        ScrollView:
            BoxLayout:
                id: detail_content
                orientation: 'vertical'
                padding: dp(15)
                spacing: dp(15)
                size_hint_y: None
                height: self.minimum_height
                
                # Product details will be populated dynamically
        
        BoxLayout:
            size_hint_y: None
            height: dp(70)
            padding: dp(15)
            spacing: dp(10)
            
            Label:
                text: f'Total: ${root.current_price:.2f}'
                font_size: dp(20)
                bold: True
                size_hint_x: 0.5
            
            Button:
                text: 'Add to Cart'
                font_size: dp(16)
                bold: True
                background_color: (0.3, 0.6, 0.3, 1)
                on_release: root.add_to_cart()

<CartScreen>:
    name: 'cart'
    BoxLayout:
        orientation: 'vertical'
        
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            padding: dp(10)
            
            Button:
                text: '← Back'
                on_release: app.root.current = 'main'
            
            Label:
                text: 'Your Cart'
                font_size: dp(18)
                bold: True
        
        BoxLayout:
            size_hint_y: None
            height: dp(40)
            padding: dp(10)
            
            Label:
                text: f'Items: {app.cart_count}'
                size_hint_x: 0.5
            
            Button:
                text: 'Clear Cart'
                size_hint_x: 0.5
                on_release: root.clear_cart()
        
        ScrollView:
            BoxLayout:
                id: cart_items
                orientation: 'vertical'
                padding: dp(10)
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height
        
        BoxLayout:
            size_hint_y: None
            height: dp(70)
            padding: dp(15)
            spacing: dp(10)
            
            Label:
                text: f'Total: ${root.cart_total:.2f}'
                font_size: dp(20)
                bold: True
                size_hint_x: 0.5
            
            Button:
                text: 'Checkout'
                font_size: dp(16)
                bold: True
                background_color: (0.3, 0.6, 0.3, 1)
                on_release: app.root.current = 'checkout'

<CheckoutScreen>:
    name: 'checkout'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(15)
        
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            
            Button:
                text: '← Back'
                on_release: app.root.current = 'cart'
            
            Label:
                text: 'Checkout'
                font_size: dp(18)
                bold: True
        
        Label:
            text: 'Order Summary'
            font_size: dp(16)
            bold: True
            size_hint_y: None
            height: dp(30)
        
        ScrollView:
            BoxLayout:
                id: order_summary
                orientation: 'vertical'
                padding: dp(10)
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height
        
        BoxLayout:
            size_hint_y: None
            height: dp(60)
            
            Label:
                text: f'Total: ${root.order_total:.2f}'
                font_size: dp(22)
                bold: True
                size_hint_x: 0.5
        
        BoxLayout:
            orientation: 'vertical'
            spacing: dp(10)
            size_hint_y: None
            height: dp(150)
            
            Label:
                text: 'Shipping Information'
                font_size: dp(14)
                bold: True
                size_hint_y: None
                height: dp(25)
            
            TextInput:
                id: shipping_name
                hint_text: 'Full Name'
                multiline: False
                size_hint_y: None
                height: dp(40)
            
            TextInput:
                id: shipping_address
                hint_text: 'Shipping Address'
                multiline: False
                size_hint_y: None
                height: dp(40)
        
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)
            
            Button:
                text: 'Cancel'
                on_release: app.root.current = 'cart'
            
            Button:
                text: 'Place Order'
                background_color: (0.3, 0.6, 0.3, 1)
                on_release: root.place_order()

<CheckoutSuccessScreen>:
    name: 'success'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(30)
        spacing: dp(20)
        
        Widget:
            size_hint_y: 0.3
        
        Label:
            text: '✓'
            font_size: dp(80)
            color: (0.3, 0.8, 0.3, 1)
            size_hint_y: None
            height: dp(100)
        
        Label:
            text: 'Order Placed Successfully!'
            font_size: dp(22)
            bold: True
            size_hint_y: None
            height: dp(40)
        
        Label:
            text: 'Thank you for your purchase.\\nYour specialty coffee is on its way!'
            font_size: dp(14)
            halign: 'center'
            size_hint_y: None
            height: dp(60)
        
        Widget:
            size_hint_y: 0.2
        
        Button:
            text: 'Continue Shopping'
            size_hint_y: None
            height: dp(50)
            font_size: dp(16)
            on_release: 
                app.reset_app()
                app.root.current = 'main'

<ToggleButton@Button>:
    active: False
    background_color: (0.8, 0.8, 0.8, 1) if not self.active else (0.3, 0.6, 0.9, 1)
    color: (0, 0, 0, 1) if not self.active else (1, 1, 1, 1)

<ProductCard@BoxLayout>:
    orientation: 'vertical'
    padding: dp(8)
    spacing: dp(5)
    canvas.before:
        Color:
            rgba: (0.95, 0.95, 0.95, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    
    Label:
        id: product_image
        text: '☕'
        font_size: dp(40)
        size_hint_y: None
        height: dp(60)
    
    Label:
        id: product_name
        text: ''
        font_size: dp(14)
        bold: True
        max_lines: 2
        size_hint_y: None
        height: dp(35)
    
    Label:
        id: product_category
        text: ''
        font_size: dp(11)
        color: (0.5, 0.5, 0.5, 1)
        size_hint_y: None
        height: dp(20)
    
    BoxLayout:
        size_hint_y: None
        height: dp(25)
        
        Label:
            id: product_price
            text: ''
            font_size: dp(14)
            bold: True
            color: (0.3, 0.6, 0.3, 1)
        
        Widget:
        
        Button:
            text: '+'
            size_hint_x: None
            width: dp(30)
            on_release: root.add_to_cart_callback()

<CartItem@BoxLayout>:
    orientation: 'horizontal'
    padding: dp(10)
    spacing: dp(10)
    size_hint_y: None
    height: dp(70)
    canvas.before:
        Color:
            rgba: (0.98, 0.98, 0.98, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    
    Label:
        text: '☕'
        font_size: dp(30)
        size_hint_x: None
        width: dp(50)
    
    BoxLayout:
        orientation: 'vertical'
        
        Label:
            id: item_name
            text: ''
            font_size: dp(14)
            bold: True
            size_hint_y: None
            height: dp(25)
        
        Label:
            id: item_price
            text: ''
            font_size: dp(12)
            color: (0.3, 0.6, 0.3, 1)
            size_hint_y: None
            height: dp(20)
    
    BoxLayout:
        orientation: 'horizontal'
        size_hint_x: None
        width: dp(100)
        spacing: dp(5)
        
        Button:
            text: '-'
            size_hint_x: 0.3
            on_release: root.decrease_quantity()
        
        Label:
            id: item_quantity
            text: '1'
            font_size: dp(16)
            halign: 'center'
            size_hint_x: 0.4
        
        Button:
            text: '+'
            size_hint_x: 0.3
            on_release: root.increase_quantity()
    
    Button:
        text: '✕'
        size_hint_x: None
        width: dp(30)
        on_release: root.remove_item()
'''


class ProductCard(BoxLayout):
    """Custom widget for displaying product information in a card format."""
    
    def __init__(self, product, **kwargs):
        super().__init__(**kwargs)
        self.product = product
        self.ids.product_name.text = product['name']
        self.ids.product_category.text = product['category'].replace('_', ' ').title()
        self.ids.product_price.text = f"${product['price']:.2f}"
    
    def add_to_cart_callback(self):
        """Callback when + button is pressed on product card."""
        app = App.get_running_app()
        app.add_to_cart(self.product)


class CartItem(BoxLayout):
    """Custom widget for displaying cart items with quantity controls."""
    
    def __init__(self, cart_item, **kwargs):
        super().__init__(**kwargs)
        self.cart_item = cart_item
        self.update_display()
    
    def update_display(self):
        """Update the display with current cart item data."""
        self.ids.item_name.text = self.cart_item['product']['name']
        self.ids.item_price.text = f"${self.cart_item['product']['price']:.2f} each"
        self.ids.item_quantity.text = str(self.cart_item['quantity'])
    
    def increase_quantity(self):
        """Increase item quantity."""
        app = App.get_running_app()
        app.update_cart_quantity(self.cart_item['product'], 1)
        self.update_display()
    
    def decrease_quantity(self):
        """Decrease item quantity."""
        app = App.get_running_app()
        app.update_cart_quantity(self.cart_item['product'], -1)
        self.update_display()
    
    def remove_item(self):
        """Remove item from cart."""
        app = App.get_running_app()
        app.remove_from_cart(self.cart_item['product'])


class MainScreen(Screen):
    """Main screen displaying products with search and filter functionality."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_products = []
        self.displayed_products = []
    
    def on_enter(self):
        """Called when screen is displayed."""
        self.load_products()
        self.filter_products('')
    
    def load_products(self):
        """Load all products."""
        app = App.get_running_app()
        self.all_products = app.products.copy()
    
    def toggle_search(self):
        """Toggle search bar visibility."""
        search_container = self.ids.search_container
        if search_container.height == 0:
            search_container.height = dp(50)
        else:
            search_container.height = 0
    
    def clear_search(self):
        """Clear search input."""
        self.ids.search_input.text = ''
    
    def filter_products(self, search_text):
        """Filter products based on search text."""
        app = App.get_running_app()
        search_text = search_text.lower()
        
        # Get current category filter
        category = self.get_current_category()
        
        filtered = []
        for product in self.all_products:
            # Apply category filter
            if category != 'all' and product['category'] != category:
                continue
            
            # Apply search filter
            if search_text and search_text not in product['name'].lower():
                continue
            
            filtered.append(product)
        
        self.display_products(filtered)
    
    def get_current_category(self):
        """Get currently selected category."""
        for btn in self.ids.category_filters.children:
            if hasattr(btn, 'active') and btn.active:
                category_map = {
                    'All': 'all',
                    'Espresso': 'espresso',
                    'Single Origin': 'single_origin',
                    'Blend': 'blend',
                    'Decaf': 'decaf'
                }
                return category_map.get(btn.text, 'all')
        return 'all'
    
    def filter_by_category(self, category):
        """Filter products by category."""
        search_text = self.ids.search_input.text
        self.filter_products(search_text)
    
    def display_products(self, products):
        """Display products in the grid."""
        grid = self.ids.products_grid
        grid.clear_widgets()
        
        for product in products:
            card = ProductCard(product)
            grid.add_widget(card)


class ProductDetailScreen(Screen):
    """Screen for displaying detailed product information."""
    
    current_product = ObjectProperty(None)
    current_quantity = NumericProperty(1)
    current_price = NumericProperty(0.0)
    
    def on_enter(self):
        """Populate product details when entering screen."""
        if self.current_product:
            self.populate_details()
    
    def populate_details(self):
        """Populate the detail content with product information."""
        content = self.ids.detail_content
        content.clear_widgets()
        
        product = self.current_product
        
        # Product image placeholder
        image_label = Label(
            text='☕',
            font_size=dp(80),
            size_hint_y=None,
            height=dp(120),
            halign='center'
        )
        content.add_widget(image_label)
        
        # Product name
        name_label = Label(
            text=product['name'],
            font_size=dp(24),
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        content.add_widget(name_label)
        
        # Category
        category_label = Label(
            text=product['category'].replace('_', ' ').title(),
            font_size=dp(14),
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=dp(25)
        )
        content.add_widget(category_label)
        
        # Price
        price_label = Label(
            text=f"${product['price']:.2f}",
            font_size=dp(28),
            bold=True,
            color=(0.3, 0.6, 0.3, 1),
            size_hint_y=None,
            height=dp(40)
        )
        content.add_widget(price_label)
        
        # Description
        desc_label = Label(
            text=product['description'],
            font_size=dp(14),
            size_hint_y=None,
            height=dp(80),
            text_size=(content.width - 30, None),
            valign='top'
        )
        content.add_widget(desc_label)
        
        # Tasting notes
        notes_label = Label(
            text=f"Tasting Notes: {product['tasting_notes']}",
            font_size=dp(13),
            italic=True,
            size_hint_y=None,
            height=dp(30)
        )
        content.add_widget(notes_label)
        
        # Quantity selector
        qty_box = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10)
        )
        
        minus_btn = Button(
            text='-',
            font_size=dp(20),
            size_hint_x=0.3
        )
        minus_btn.bind(on_release=lambda x: self.adjust_quantity(-1))
        
        qty_label = Label(
            text=str(self.current_quantity),
            font_size=dp(20),
            halign='center',
            size_hint_x=0.4
        )
        
        plus_btn = Button(
            text='+',
            font_size=dp(20),
            size_hint_x=0.3
        )
        plus_btn.bind(on_release=lambda x: self.adjust_quantity(1))
        
        qty_box.add_widget(minus_btn)
        qty_box.add_widget(qty_label)
        qty_box.add_widget(plus_btn)
        
        content.add_widget(qty_box)
        
        # Update current price
        self.current_price = product['price'] * self.current_quantity
    
    def adjust_quantity(self, delta):
        """Adjust product quantity."""
        self.current_quantity = max(1, self.current_quantity + delta)
        self.current_price = self.current_product['price'] * self.current_quantity
        self.populate_details()
    
    def add_to_cart(self):
        """Add product to cart with selected quantity."""
        app = App.get_running_app()
        for _ in range(self.current_quantity):
            app.add_to_cart(self.current_product)
        
        self.current_quantity = 1
        self.current_price = self.current_product['price']
        app.root.current = 'main'


class CartScreen(Screen):
    """Screen for displaying and managing cart items."""
    
    cart_total = NumericProperty(0.0)
    
    def on_enter(self):
        """Populate cart when entering screen."""
        self.populate_cart()
    
    def populate_cart(self):
        """Populate cart items display."""
        content = self.ids.cart_items
        content.clear_widgets()
        
        app = App.get_running_app()
        total = 0.0
        
        for cart_item in app.cart:
            item_widget = CartItem(cart_item)
            content.add_widget(item_widget)
            total += cart_item['product']['price'] * cart_item['quantity']
        
        self.cart_total = total
    
    def clear_cart(self):
        """Clear all items from cart."""
        app = App.get_running_app()
        app.cart.clear()
        self.populate_cart()


class CheckoutScreen(Screen):
    """Screen for checkout process."""
    
    order_total = NumericProperty(0.0)
    
    def on_enter(self):
        """Populate order summary when entering screen."""
        self.populate_summary()
    
    def populate_summary(self):
        """Populate order summary."""
        content = self.ids.order_summary
        content.clear_widgets()
        
        app = App.get_running_app()
        total = 0.0
        
        for cart_item in app.cart:
            item_total = cart_item['product']['price'] * cart_item['quantity']
            total += item_total
            
            item_box = BoxLayout(
                size_hint_y=None,
                height=dp(30)
            )
            
            name_label = Label(
                text=f"{cart_item['product']['name']} x{cart_item['quantity']}",
                font_size=dp(14),
                halign='left'
            )
            
            price_label = Label(
                text=f"${item_total:.2f}",
                font_size=dp(14),
                bold=True,
                halign='right'
            )
            
            item_box.add_widget(name_label)
            item_box.add_widget(price_label)
            content.add_widget(item_box)
        
        # Add subtotal
        subtotal_box = BoxLayout(
            size_hint_y=None,
            height=dp(30)
        )
        subtotal_box.add_widget(Label(text='Subtotal:', halign='left'))
        subtotal_box.add_widget(Label(text=f'${total:.2f}', bold=True, halign='right'))
        content.add_widget(subtotal_box)
        
        # Add shipping
        shipping_box = BoxLayout(
            size_hint_y=None,
            height=dp(30)
        )
        shipping_box.add_widget(Label(text='Shipping:', halign='left'))
        shipping_box.add_widget(Label(text='$5.00', bold=True, halign='right'))
        content.add_widget(shipping_box)
        
        # Add total
        self.order_total = total + 5.0
        total_box = BoxLayout(
            size_hint_y=None,
            height=dp(35)
        )
        total_box.add_widget(Label(text='Total:', font_size=dp(16), bold=True, halign='left'))
        total_box.add_widget(Label(text=f'${self.order_total:.2f}', font_size=dp(16), bold=True, halign='right'))
        content.add_widget(total_box)
    
    def place_order(self):
        """Simulate placing an order."""
        name = self.ids.shipping_name.text
        address = self.ids.shipping_address.text
        
        # Simple validation
        if not name or not address:
            # Show error (in a real app, use a popup)
            return
        
        # Clear cart and navigate to success screen
        app = App.get_running_app()
        app.cart.clear()
        app.root.current = 'success'


class CheckoutSuccessScreen(Screen):
    """Screen displayed after successful checkout."""
    pass


class SpecialtyCoffeeApp(App):
    """Main application class for the Specialty Coffee E-Commerce App."""
    
    cart_count = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cart = []
        self.products = [
            {
                'id': 1,
                'name': 'Ethiopian Yirgacheffe',
                'category': 'single_origin',
                'price': 18.99,
                'description': 'A bright and floral single origin coffee from Ethiopia with notes of bergamot and jasmine.',
                'tasting_notes': 'Floral, Citrus, Tea-like'
            },
            {
                'id': 2,
                'name': 'Colombian Supremo',
                'category': 'single_origin',
                'price': 16.99,
                'description': 'A well-balanced Colombian coffee with caramel sweetness and nutty undertones.',
                'tasting_notes': 'Caramel, Nutty, Balanced'
            },
            {
                'id': 3,
                'name': 'Espresso Roast Blend',
                'category': 'espresso',
                'price': 15.99,
                'description': 'Our signature espresso blend with rich crema and bold chocolate flavors.',
                'tasting_notes': 'Chocolate, Bold, Creamy'
            },
            {
                'id': 4,
                'name': 'Morning Blend',
                'category': 'blend',
                'price': 14.99,
                'description': 'A smooth and approachable blend perfect for starting your day.',
                'tasting_notes': 'Smooth, Mild, Sweet'
            },
            {
                'id': 5,
                'name': 'Sumatra Mandheling',
                'category': 'single_origin',
                'price': 17.99,
                'description': 'A full-bodied Indonesian coffee with earthy and spicy characteristics.',
                'tasting_notes': 'Earthy, Spicy, Full-bodied'
            },
            {
                'id': 6,
                'name': 'Swiss Water Decaf',
                'category': 'decaf',
                'price': 16.99,
                'description': 'Chemical-free decaffeinated coffee that retains all the flavor.',
                'tasting_notes': 'Clean, Smooth, Rich'
            }
        ]
    
    def build(self):
        """Build and return the app UI."""
        self.title = 'Specialty Coffee Shop'
        Builder.load_string(KV)
        sm = ScreenManager()
        return sm
    
    def on_start(self):
        """Initialize app state."""
        self.update_cart_count()
    
    def add_to_cart(self, product):
        """Add a product to the cart."""
        # Check if product already in cart
        for item in self.cart:
            if item['product']['id'] == product['id']:
                item['quantity'] += 1
                self.update_cart_count()
                return
        
        # Add new item to cart
        self.cart.append({
            'product': product,
            'quantity': 1
        })
        self.update_cart_count()
    
    def update_cart_quantity(self, product, delta):
        """Update quantity of a product in cart."""
        for item in self.cart:
            if item['product']['id'] == product['id']:
                item['quantity'] += delta
                if item['quantity'] <= 0:
                    self.cart.remove(item)
                break
        self.update_cart_count()
    
    def remove_from_cart(self, product):
        """Remove a product from cart."""
        for item in self.cart:
            if item['product']['id'] == product['id']:
                self.cart.remove(item)
                break
        self.update_cart_count()
    
    def update_cart_count(self):
        """Update the cart count property."""
        total = sum(item['quantity'] for item in self.cart)
        self.cart_count = total
    
    def reset_app(self):
        """Reset app state after checkout."""
        self.cart.clear()
        self.update_cart_count()
    
    def show_product_detail(self, product):
        """Navigate to product detail screen."""
        detail_screen = self.root.get_screen('detail')
        detail_screen.current_product = product
        detail_screen.current_quantity = 1
        detail_screen.current_price = product['price']
        self.root.current = 'detail'


# Import required Kivy classes
from kivy.uix.label import Label
from kivy.metrics import dp

if __name__ == '__main__':
    SpecialtyCoffeeApp().run()
