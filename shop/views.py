from django.shortcuts import render
from django.http import Http404


COMPLETE_PRODUCTS = [
    {
        "slug": "element-section-complete",
        "brand": "ELEMENT",
        "name": "Section Complete",
        "level": "Beginner",
        "title": "ELEMENT SECTION COMPLETE SKATEBOARD",
        "description": '8.0" Street Skateboard',
        "long_description": "The Element Section Complete is built for skaters who want a reliable and comfortable ride right out of the box.",
        "width": "w80",
        "width_label": '8.0" and above',
        "price_number": 129,
        "price": "$129",
        "rating": "4.8",
        "reviews": 32,
        "image": "images/catalog/complete1.png",
        "gallery": [
            "images/catalog/complete1.png",
            "images/catalog/complete1.png",
            "images/catalog/complete1.png",
            "images/catalog/complete1.png",
        ],
        "specs": [
            'Deck Width: 8.0"',
            "Deck Material: 7-ply maple",
            "Trucks: Element standard trucks",
        ],
    },
    {
        "slug": "santa-cruz-classic-complete",
        "brand": "SANTA CRUZ",
        "name": "Classic Dot Complete",
        "level": "Beginner",
        "title": "SANTA CRUZ CLASSIC COMPLETE SKATEBOARD",
        "description": '7.0" Street Skateboard',
        "long_description": "The Santa Cruz Classic Dot is a time-tested classic, perfect for both beginners and experienced riders. This complete setup offers reliability, style and a smooth ride.",
        "width": "w75",
        "width_label": '7.5"',
        "price_number": 134,
        "price": "$134",
        "rating": "4.8",
        "reviews": 32,
        "image": "images/catalog/complete2.png",
        "gallery": [
            "images/catalog/complete2.png",
            "images/catalog/complete2.png",
            "images/catalog/complete2.png",
            "images/catalog/complete2.png",
        ],
        "specs": [
            'Deck Width: 7.5"',
            "Deck Material: 7-ply maple",
            "Trucks: Standard polished trucks",
        ],
    },
    {
        "slug": "plan-b-team-complete",
        "brand": "PLAN B",
        "name": "Team Complete",
        "level": "Intermediate",
        "title": "PLAN B TEAM COMPLETE SKATEBOARD",
        "description": '7.0" Street Skateboard',
        "long_description": "Plan B Team Complete is a strong everyday board for street riding and park sessions.",
        "width": "w75",
        "width_label": '7.5"',
        "price_number": 119,
        "price": "$119",
        "rating": "4.7",
        "reviews": 21,
        "image": "images/catalog/complete3.png",
        "gallery": [
            "images/catalog/complete3.png",
            "images/catalog/complete3.png",
            "images/catalog/complete3.png",
            "images/catalog/complete3.png",
        ],
        "specs": [
            'Deck Width: 7.0"',
            "Deck Material: 7-ply maple",
            "Wheels: Street wheels",
        ],
    },
    {
        "slug": "almost-yuri-pro",
        "brand": "ALMOST",
        "name": "Yuri Pro",
        "level": "Intermediate",
        "title": "ALMOST YURI PRO COMPLETE SKATEBOARD",
        "description": '8.0" Street Skateboard',
        "long_description": "Almost Yuri Pro is a fun and stable complete skateboard with a playful graphic and solid construction.",
        "width": "w80",
        "width_label": '8.0" and above',
        "price_number": 144,
        "price": "$144",
        "rating": "4.9",
        "reviews": 18,
        "image": "images/catalog/complete4.png",
        "gallery": [
            "images/catalog/complete4.png",
            "images/catalog/complete4.png",
            "images/catalog/complete4.png",
            "images/catalog/complete4.png",
        ],
        "specs": [
            'Deck Width: 8.0"',
            "Deck Material: 7-ply maple",
            "Level: Beginner / Intermediate",
        ],
    },
    {
        "slug": "zero-thomas-cross-pro",
        "brand": "ZERO",
        "name": "Thomas ‘Cross’ Pro",
        "level": "Pro",
        "title": "ZERO THOMAS CROSS PRO SKATEBOARD",
        "description": '8.0" Street Skateboard',
        "long_description": "Zero Thomas Cross Pro is a bold complete setup with a classic black graphic and strong street-ready build.",
        "width": "w80",
        "width_label": '8.0" and above',
        "price_number": 120,
        "price": "$120",
        "rating": "4.8",
        "reviews": 27,
        "image": "images/catalog/complete5.png",
        "gallery": [
            "images/catalog/complete5.png",
            "images/catalog/complete5.png",
            "images/catalog/complete5.png",
            "images/catalog/complete5.png",
        ],
        "specs": [
            'Deck Width: 8.0"',
            "Deck Material: 7-ply maple",
            "Graphic: Zero skull",
        ],
    },
    {
        "slug": "element-section",
        "brand": "ELEMENT",
        "name": "Section",
        "level": "Beginner",
        "title": "ELEMENT SECTION SKATEBOARD",
        "description": '8.0" Street Skateboard',
        "long_description": "Element Section is a reliable complete board for everyday skating.",
        "width": "w80",
        "width_label": '8.0" and above',
        "price_number": 129,
        "price": "$129",
        "rating": "4.7",
        "reviews": 19,
        "image": "images/catalog/complete6.png",
        "gallery": [
            "images/catalog/complete6.png",
            "images/catalog/complete6.png",
            "images/catalog/complete6.png",
            "images/catalog/complete6.png",
        ],
        "specs": [
            'Deck Width: 8.0"',
            "Deck Material: 7-ply maple",
            "Trucks: Standard trucks",
        ],
    },
    {
        "slug": "baker-logo-red-complete",
        "brand": "BAKER",
        "name": "Logo Red Complete",
        "level": "Intermediate",
        "title": "BAKER LOGO RED COMPLETE SKATEBOARD",
        "description": '7.75" Street Skateboard',
        "long_description": "Baker Logo Red Complete is made for riders who want a classic street skateboarding feel.",
        "width": "w775",
        "width_label": '7.75"',
        "price_number": 115,
        "price": "$115",
        "rating": "4.6",
        "reviews": 14,
        "image": "images/catalog/complete7.png",
        "gallery": [
            "images/catalog/complete7.png",
            "images/catalog/complete7.png",
            "images/catalog/complete7.png",
            "images/catalog/complete7.png",
        ],
        "specs": [
            'Deck Width: 7.75"',
            "Deck Material: 7-ply maple",
            "Style: Street",
        ],
    },
    {
        "slug": "girl-kennedy-sanrio",
        "brand": "GIRL",
        "name": "Kennedy “Sanrio” Collab",
        "level": "Intermediate",
        "title": "GIRL KENNEDY SANRIO COLLAB SKATEBOARD",
        "description": '8.0" Street Skateboard',
        "long_description": "Girl Kennedy Sanrio Collab is a colorful complete board with a collectible graphic.",
        "width": "w80",
        "width_label": '8.0" and above',
        "price_number": 120,
        "price": "$120",
        "rating": "4.9",
        "reviews": 24,
        "image": "images/catalog/complete8.png",
        "gallery": [
            "images/catalog/complete8.png",
            "images/catalog/complete8.png",
            "images/catalog/complete8.png",
            "images/catalog/complete8.png",
        ],
        "specs": [
            'Deck Width: 8.0"',
            "Deck Material: 7-ply maple",
            "Graphic: Sanrio collaboration",
        ],
    },
    {
        "slug": "habitat-wood-series-wall",
        "brand": "HABITAT",
        "name": "Wood Series Wall Graphic",
        "level": "Beginner",
        "title": "HABITAT WOOD SERIES WALL GRAPHIC SKATEBOARD",
        "description": '8.0" Street Skateboard',
        "long_description": "Habitat Wood Series is a clean and natural-looking complete skateboard with a premium feel.",
        "width": "w80",
        "width_label": '8.0" and above',
        "price_number": 110,
        "price": "$110",
        "rating": "4.7",
        "reviews": 16,
        "image": "images/catalog/complete9.png",
        "gallery": [
            "images/catalog/complete9.png",
            "images/catalog/complete9.png",
            "images/catalog/complete9.png",
            "images/catalog/complete9.png",
        ],
        "specs": [
            'Deck Width: 8.0"',
            "Deck Material: 7-ply maple",
            "Style: Complete skateboard",
        ],
    },
    {
        "slug": "element-art-series-sloth",
        "brand": "ELEMENT",
        "name": "Art Series - Sloth",
        "level": "Beginner",
        "title": "ELEMENT ART SERIES SLOTH SKATEBOARD",
        "description": '7.75" Street Skateboard',
        "long_description": "Element Art Series Sloth is a stylish complete board with a unique illustration.",
        "width": "w775",
        "width_label": '7.75"',
        "price_number": 115,
        "price": "$115",
        "rating": "4.8",
        "reviews": 20,
        "image": "images/catalog/complete10.png",
        "gallery": [
            "images/catalog/complete10.png",
            "images/catalog/complete10.png",
            "images/catalog/complete10.png",
            "images/catalog/complete10.png",
        ],
        "specs": [
            'Deck Width: 7.75"',
            "Deck Material: 7-ply maple",
            "Graphic: Sloth art series",
        ],
    },
    {
        "slug": "anti-hero-pigeon-olive",
        "brand": "ANTI HERO",
        "name": "Pigeon - Olive Green",
        "level": "Pro",
        "title": "ANTI HERO PIGEON OLIVE GREEN SKATEBOARD",
        "description": '7.0" Street Skateboard',
        "long_description": "Anti Hero Pigeon is a classic complete board with a minimal olive-green graphic.",
        "width": "w75",
        "width_label": '7.5"',
        "price_number": 133,
        "price": "$133",
        "rating": "4.6",
        "reviews": 11,
        "image": "images/catalog/complete11.png",
        "gallery": [
            "images/catalog/complete11.png",
            "images/catalog/complete11.png",
            "images/catalog/complete11.png",
            "images/catalog/complete11.png",
        ],
        "specs": [
            'Deck Width: 7.0"',
            "Deck Material: 7-ply maple",
            "Graphic: Pigeon",
        ],
    },
    {
        "slug": "habitat-magazine-logo-red",
        "brand": "HABITAT",
        "name": "Magazine Logo - Red",
        "level": "Pro",
        "title": "HABITAT MAGAZINE LOGO RED SKATEBOARD",
        "description": '8.0" Street Skateboard',
        "long_description": "Habitat Magazine Logo Red is a strong complete skateboard with bold red graphics.",
        "width": "w80",
        "width_label": '8.0" and above',
        "price_number": 100,
        "price": "$100",
        "rating": "4.5",
        "reviews": 9,
        "image": "images/catalog/complete12.png",
        "gallery": [
            "images/catalog/complete12.png",
            "images/catalog/complete12.png",
            "images/catalog/complete12.png",
            "images/catalog/complete12.png",
        ],
        "specs": [
            'Deck Width: 8.0"',
            "Deck Material: 7-ply maple",
            "Color: Red",
        ],
    },
]


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


def complete_skateboards(request):
    selected_brands = request.GET.getlist("brand")
    selected_levels = request.GET.getlist("level")
    selected_widths = request.GET.getlist("width")

    min_price = request.GET.get("min_price", "59")
    max_price = request.GET.get("max_price", "503")

    try:
        min_price_number = int(min_price)
    except ValueError:
        min_price_number = 59

    try:
        max_price_number = int(max_price)
    except ValueError:
        max_price_number = 503

    filtered_products = []

    for product in COMPLETE_PRODUCTS:
        brand_matches = not selected_brands or product["brand"] in selected_brands
        level_matches = not selected_levels or product.get("level") in selected_levels
        width_matches = not selected_widths or product["width"] in selected_widths
        price_matches = min_price_number <= product["price_number"] <= max_price_number

        if brand_matches and level_matches and width_matches and price_matches:
                    filtered_products.append(product)

    active_filters_count = len(selected_brands) + len(selected_levels) + len(selected_widths)

    if min_price_number != 59 or max_price_number != 503:
        active_filters_count += 1

    return render(request, 'shop/complete_skateboards.html', {
    'products': filtered_products,
    'selected_brands': selected_brands,
    'selected_levels': selected_levels,
    'selected_widths': selected_widths,
    'min_price': min_price_number,
    'max_price': max_price_number,
    'active_filters_count': active_filters_count,
})


def product_detail(request, slug):
    product = None

    for item in COMPLETE_PRODUCTS:
        if item["slug"] == slug:
            product = item
            break

    if product is None:
        raise Http404("Product not found")

    related_products = []

    for item in COMPLETE_PRODUCTS:
        if item["slug"] != slug:
            related_products.append(item)

    related_products = related_products[:4]

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })