"use strict"

const updateState = async (productCard) => {
  const productId = productCard.dataset.productId
  await fetch(`/delete-product-session/${productId}`)
}

const container = document.getElementById('container');
for (let i = 0; i<container.childNodes.length; i++) {
  let deleteBtn= document.getElementById('deleteButton'+i);
  let buyBtn = document.getElementById('buyButton'+i);
  let productCard = document.getElementById('productCard'+i);
  let count = document.getElementById('count'+i);
  let price = document.getElementById('price'+i);

  count.addEventListener('change', function() {
    let v = parseInt(this.value);
    let max = parseInt(this.dataset.max);
    let productPrice = parseInt(this.dataset.price);
    if (v < 1 || isNaN(v)) this.value = 1;
    if (v > max) this.value = max;
    price.innerHTML = this.value * productPrice + ' ₽';
  })

  deleteBtn.addEventListener('click', ()=>{
    updateState(productCard)
    productCard.remove()
  })

  buyBtn.addEventListener('click', ()=>{
    alert("Товар успешно оплачен")
    updateState(productCard)
    productCard.remove()
  })
};

