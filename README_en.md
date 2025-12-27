# ProductOi — Food Delivery Service

A modern demo web platform for ordering food 24/7. Clean UI with a purple-and-white theme.

## Features

- Catalog of dishes organized by category
- Shopping cart with add/remove and quantity control
- Delivery options (express, standard, pickup)
- Payment options: Card, Cash, Apple Pay, Google Pay
- Responsive design for mobile and desktop

## Tech stack

- Backend: Python + Flask
- Frontend: HTML5, CSS3, vanilla JavaScript
- Templating: Jinja2

## Project structure

```
ProductOi/
├── app/
│   ├── __init__.py           # Flask app initialization
│   ├── routes.py             # Routes and core logic
│   ├── templates/            # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── cart.html
│   │   └── checkout.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   └── script.js
│       └── images/
├── run.py
├── requirements.txt
├── README.md                 # Short project README (index)
├── README_en.md              # This English README (detailed)
└── README_uk.md              # Ukrainian README (detailed)
```

## Quick start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the app:

```bash
python run.py
```

3. Open in your browser:

```
http://localhost:5000
```

## Pages and functionality

- **Home / Catalog** — Browse available dishes, filter by category, choose quantity and add to cart.
- **Cart** — See cart items, change quantity, remove items, view subtotal.
- **Checkout** — Enter customer details, choose delivery and payment method, place order.

## Images and translations

- Product images are currently loaded from public image URLs (Unsplash queries). For reliability, you can replace these with local files under `app/static/images`.
- This repository includes both detailed English (`README_en.md`) and Ukrainian (`README_uk.md`) READMEs.

## Libraries

- Flask==2.3.2
- Werkzeug==2.3.6
- Jinja2==3.1.2

## Future improvements

- Use a real database (PostgreSQL, MySQL, or MongoDB)
- User accounts and order history
- Payment provider integration (Stripe, Adyen, etc.)
- Admin panel and product management

---