itemList = document.getElementById("item_list")
exampleItemNode = document.getElementById("item_example")

cartList = document.getElementById("cart_list")
exampleCartNode = document.getElementById("cart_example")
cartCheckout = document.getElementById("cart_checkout")

itemDataJSON = document.getElementById("item_data").innerText
itemData = JSON.parse(itemDataJSON)

function round_to(num, decimal) {
    // Workaround for rounding to 2 decimals. JS is stupid lmao
    return Math.round(num * (10 ** decimal)) / (10 ** decimal)
}

function post(data, route=null, method='post') {
    // Creates an invisible form to submit data
    const form = document.createElement('form')
    form.method = method
    if (route !== null)
        form.action = route

    for (const key in data) {
        const inputField = document.createElement('input')
        inputField.type = 'hidden'
        inputField.name = key
        inputField.name = data[key]

        form.appendChild(inputField)
    }

    document.body.appendChild(form)
    form.submit()
}

function parseCartToObject() {
    const obj = {}

    document.getElementsByName("cart_entry").forEach(node => {
        if (node.classList.contains("is-hidden")) return
        name = node.querySelector("[name=cart_name]").innerText
        quantity = parseInt(node.querySelector("[name=cart_quantity]").innerText)
        obj[name] = quantity
    })

    return obj
}

function cartUpdateTotal() {
    total = 0
    document.getElementsByName("cart_entry").forEach(node => {
        if (node.classList.contains("is-hidden")) return
        totalNode = node.querySelector("[name=cart_total]")
        total_num = parseFloat(totalNode.innerText.slice(1))
        total += total_num
    })

    cartTotalNum = document.getElementById("cart_total")
    cartTotalNum.innerText = "$" + round_to(total, 2)
}

function cartUpdateEntryTotal(node, price) {
    quantityNode = node.querySelector("[name=cart_quantity]")
    totalNode = node.querySelector("[name=cart_total]")

    quantity = parseInt(quantityNode.innerText)

    totalNode.innerText = "$" + round_to(price * quantity, 2)
}

function addItemToCart(itemName, quantity) {
    console.log("Adding " + itemName + " to cart")
    const available = itemData[itemName].available
    const price = itemData[itemName].price
    node = cartList.querySelector("[id=cart_" + itemName + "]")
    console.log(node)

    if (node === null) {
        node = exampleCartNode.cloneNode(deep=true)
        
        node.id = "cart_" + itemName
        node.classList.remove("is-hidden")
        
        node.querySelector("[name=cart_name]").innerText = itemName

        const parentNode = node
        const quantityNode = node.querySelector("[name=cart_quantity]")
        const plusNode = node.querySelector("[name=cart_plus]")
        const minusNode = node.querySelector("[name=cart_minus]")
        const removeNode = node.querySelector("[name=cart_remove]")

        plusNode.addEventListener("click", function(){
            num = parseInt(quantityNode.innerText)
            if (num + 1 <= available) {
                quantityNode.innerText = ++num
                cartUpdateEntryTotal(parentNode, price)
                cartUpdateTotal()
            }
        })
        minusNode.addEventListener("click", function(){
            num = parseInt(quantityNode.innerText)
            if (0 < num - 1) {
                quantityNode.innerText = --num
                cartUpdateEntryTotal(parentNode, price)
                cartUpdateTotal()
            }
        })
        removeNode.addEventListener("click", function(){
            parentNode.remove()
        })

        cartList.insertBefore(node, exampleCartNode)
    }

    quantityNode = node.querySelector("[name=cart_quantity]")
    totalNode = node.querySelector("[name=cart_total]")
    
    quantityOld = parseInt(quantityNode.innerText)
    quantityNew = Math.min(available, quantityOld + quantity)
    quantityNode.innerText = quantityNew
    cartUpdateEntryTotal(node, price)
    cartUpdateTotal()
}

for (const name in itemData) {
    console.log("Adding " + name)
    data = itemData[name]
    newNode = exampleItemNode.cloneNode(deep=true)

    newNode.id = "item_" + name
    newNode.classList.remove("is-hidden")

    newNode.querySelector("[name=item_name]").innerText = name
    newNode.querySelector("[name=item_available]").innerText = data.available
    newNode.querySelector("[name=item_price]").innerText = data.price

    quantityNode = newNode.querySelector("[name=item_quantity]")
    plusNode = newNode.querySelector("[name=item_plus]")
    minusNode = newNode.querySelector("[name=item_minus]")
    addNode = newNode.querySelector("[name=item_add]");

    // Trick to have listeners for each entry point to its own quantity node
    // This works because functions have its own scope hence own variable value
    // TODO: Rewrite the entire logic as function to eliminate this part
    (function() {
        var itemName = name
        var target = quantityNode
        var available = data['available']

        plusNode.addEventListener("click", function(){
            num = parseInt(target.innerText)
            if (num + 1 <= available)
                target.innerText = num + 1
        })
        minusNode.addEventListener("click", function(){
            num = parseInt(target.innerText)
            if (0 < num - 1)
                target.innerText = num - 1
        })
        addNode.addEventListener("click", function(){
            num = parseInt(target.innerText)
            addItemToCart(itemName, num)
        })
    })();

    itemList.insertBefore(newNode, exampleItemNode)
}

cartCheckout.addEventListener("click", function() {
    cart = parseCartToObject()
    console.log(cart)
    post(cart)
})

exampleItemNode.remove()
