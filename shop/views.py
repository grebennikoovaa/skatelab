from django.shortcuts import render


def home(request):
    products = [
        {
            "brand": "ELEMENT SECTION COMPLETE",
            "description": '8.0" Street Skateboard',
            "price": "$129",
            "image": "images/products/product1.png",
        },
        {
            "brand": "SANTA CRUZ CLASSIC DECK",
            "description": '8.25" Maple Deck',
            "price": "$79",
            "image": "images/products/product2.png",
        },
        {
            "brand": "INDEPENDENT STAGE 11 TRUCKS",
            "description": "Standard Polished",
            "price": "$59",
            "image": "images/products/product3.png",
        },
        {
            "brand": "SPITFIRE FORMULA FOUR WHEELS",
            "description": "52mm / 99A",
            "price": "$69",
            "image": "images/products/product4.png",
        },
        {
            "brand": "BONES REDS BEARINGS",
            "description": "ABEC 7",
            "price": "$39",
            "image": "images/products/product5.png",
        },
        {
            "brand": "MOB GRIP TAPE",
            "description": "Black Standard",
            "price": "$20",
            "image": "images/products/product6.png",
        },
        {
            "brand": "ZERO COMPLETE SKATEBOARD",
            "description": '8.125"',
            "price": "$119",
            "image": "images/products/product7.png",
        },
        {
            "brand": "SKATE TOOL MULTI KIT",
            "description": "All-in-one-tool",
            "price": "$24",
            "image": "images/products/product8.png",
        },
    ]

    return render(request, 'shop/home.html', {
        'products': products
    })