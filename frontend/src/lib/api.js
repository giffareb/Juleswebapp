const BASE_URL = 'http://localhost:8000'; // As defined in docker-compose

export async function getProducts() {
  const response = await fetch(`${BASE_URL}/api/products`);
  if (!response.ok) {
    throw new Error('Failed to fetch products');
  }
  return await response.json();
}

export async function createProduct(product) {
  const response = await fetch(`${BASE_URL}/api/products`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(product),
  });
  if (!response.ok) {
    throw new Error('Failed to create product');
  }
  return await response.json();
}

export async function createSale(sale) {
    const response = await fetch(`${BASE_URL}/api/sales`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(sale),
    });
    if (!response.ok) {
      throw new Error('Failed to create sale');
    }
    return await response.json();
}

export async function getPromptPayPayload(amount) {
    const response = await fetch(`${BASE_URL}/api/payment/promptpay`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ amount }),
      });
      if (!response.ok) {
        throw new Error('Failed to get PromptPay payload');
      }
      return await response.json();
}
