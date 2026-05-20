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
            "description": "8.25 Maple Deck",
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
            "brand": "MOP GRIP TAPE",
            "description": "Black standard",
            "price": "$20",
            "image": "images/products/product6.png",
        },

         {
            "brand": "ZERO COMPLETE SKATE",
            "description": "8.125",
            "price": "$119",
            "image": "images/products/product7.png",
        },

        {
            "brand": "Skate Tool Multi Kit",
            "description": "All-in-one-tool",
            "price": "$20",
            "image": "images/products/product8.png",
        },
    ]

    return render(request, 'shop/home.html', {
        'products': products
    })


def categories(request):
    categories_list = [
        {
            "title": "COMPLETE SKATEBOARDS",
            "count": 80,
            "image": "images/categories/complete skateboards.jpg",
        },
        {
            "title": "DECKS",
            "count": 56,
            "image": "images/categories/decks.jpg",
        },
        {
            "title": "TRUCKS",
            "count": 64,
            "image": "images/categories/trucks.jpg",
        },
        {
            "title": "WHEELS",
            "count": 68,
            "image": "images/categories/wheels.jpg",
        },
        {
            "title": "BEARINGS",
            "count": 32,
            "image": "images/categories/bearings.jpg",
        },
        {
            "title": "GRIP TAPE",
            "count": 22,
            "image": "images/categories/griptape.jpg",
        },
        {
            "title": "HARDWARE",
            "count": 19,
            "image": "images/categories/hardware.jpg",
        },
        {
            "title": "ACCESSORIES",
            "count": 45,
            "image": "images/categories/accessories.jpg",
        },
        {
            "title": "OUTLET",
            "count": 24,
            "image": "images/categories/outlet.jpg",
        },
    ]

    return render(request, 'shop/categories.html', {
        'categories': categories_list
    })