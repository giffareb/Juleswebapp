<script>
    import ProductList from '$lib/components/ProductList.svelte';
    import Cart from '$lib/components/Cart.svelte';

    let cartItems = [];

    function handleAddToCart(event) {
        const productToAdd = event.detail;
        const existingItem = cartItems.find(item => item.id === productToAdd.id);

        if (existingItem) {
            // Increment quantity
            cartItems = cartItems.map(item =>
                item.id === productToAdd.id ? { ...item, quantity: item.quantity + 1 } : item
            );
        } else {
            // Add new item
            cartItems = [...cartItems, { ...productToAdd, quantity: 1 }];
        }
    }

    function handleUpdateQuantity(event) {
        const updatedItem = event.detail;
        cartItems = cartItems.map(item =>
            item.id === updatedItem.id ? updatedItem : item
        );
    }

    function handleRemoveItem(event) {
        const itemToRemove = event.detail;
        cartItems = cartItems.filter(item => item.id !== itemToRemove.id);
    }

    function handleClearCart() {
        cartItems = [];
    }
</script>

<main class="container mx-auto p-4 sm:p-6 lg:p-8 bg-gray-100 min-h-screen">
    <header class="text-center mb-8">
        <h1 class="text-4xl font-extrabold text-gray-800">Modern POS System</h1>
        <p class="text-gray-600">Powered by FastAPI, SvelteKit, and PromptPay</p>
    </header>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2">
            <ProductList on:addToCart={handleAddToCart} />
        </div>
        <div class="lg:col-span-1">
            <Cart
                items={cartItems}
                on:updateQuantity={handleUpdateQuantity}
                on:removeItem={handleRemoveItem}
                on:clearCart={handleClearCart}
            />
        </div>
    </div>
</main>
